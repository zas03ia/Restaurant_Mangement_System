from rest_framework import serializers
from django.db import transaction
from menu.models import Item, Modifier
from order.models import Order, OrderItem
from accountio.models import Location

from shared.utils import get_organization
from order.choices import OrderStatusChoices
from transactionio.utils import create_payment
from transactionio.choices import PaymentMethodChoices, PaymentStatusChoices
from transactionio.models import Transaction


class OrderItemSerializer(serializers.ModelSerializer):
    selected_items = serializers.UUIDField(write_only=True)  # item uid
    selected_modifiers = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    location = serializers.UUIDField(write_only=True)
    item_quantity = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = OrderItem
        fields = [
            "uid",
            "item",
            "quantity",
            "modifiers",
            "selected_items",
            "selected_modifiers",
            "item_quantity",
            "location",
        ]
        read_only_fields = ["uid", "item", "quantity", "modifiers"]

    def __get_item(self, validated_data, organization):
        item_uid = validated_data.pop("selected_items")
        item_quantity = validated_data.pop("item_quantity", 1)

        # Fetch the item with item_uid
        try:
            item = Item.objects.get(
                uid=item_uid, category__menu__organization=organization
            )
        except Item.DoesNotExist:
            raise serializers.ValidationError("Invalid item UID.")

        # Check if enough stock is available for given item
        if item.quantity < item_quantity:
            raise serializers.ValidationError("Not enough quantity in stock.")

        return (item, item_quantity)

    def __get_modifiers(self, validated_data):

        modifiers_uids = validated_data.pop("selected_modifiers", [])

        # Fetch and validate modifiers
        modifiers = []
        if modifiers_uids:
            modifiers = Modifier.objects.filter(uid__in=modifiers_uids)
            if len(modifiers) != len(modifiers_uids):  # check if all uids are valid
                raise serializers.ValidationError(
                    "One or more invalid modifier UIDs provided."
                )
        return modifiers

    def __get_location(self, validated_data):
        try:
            location_uid = validated_data.pop("location")
            location = Location.objects.get(uid=location_uid)
            return location
        except Location.DoesNotExist:
            raise serializers.ValidationError("Invalid location UID.")

    @transaction.atomic
    def create(self, validated_data):
        """
        Here orderitem instance is created. If there is any existing order in cart state,
        then the new item is part of that order, otherwise, new order instance is created in cart state.
        """
        organization = get_organization(self.context["request"])
        item, item_quantity = self.__get_item(validated_data)

        # Get modifiers
        modifiers = self.__get_modifiers(validated_data, organization)

        # Calculate base price
        price = item.price * item_quantity + sum(
            [modifier.price for modifier in modifiers]
        )
        # Add vat value to price
        price += price * organization.vat / 100

        # Get location
        location = self.__get_location(validated_data)

        # Fetch or create the order in CART status
        try:
            order, created = Order.objects.get_or_create(
                organization=organization,
                user=self.context["request"].user,
                status=OrderStatusChoices.CART,
                defaults={"total_price": price, "delivery_location": location},
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Failed to fetch or create cart: {str(e)}"
            )

        # Create the OrderItem and link modifiers
        order_item = OrderItem.objects.create(
            order=order,
            item=item,
            quantity=item_quantity,
        )
        if modifiers:
            order_item.modifiers.set(modifiers)

        return order_item

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Here existing orderitem instance is updated along with some information about order in cart
        """
        organization = get_organization(self.context["request"])
        item, item_quantity = self.__get_item(validated_data)

        # Get modifiers
        modifiers = self.__get_modifiers(validated_data, organization)

        # Calculate base price
        price = item.price * item_quantity + sum(
            [modifier.price for modifier in modifiers]
        )
        # Add vat value to price
        price += price * organization.vat / 100

        # Update the OrderItem
        instance.item = item
        instance.quantity = item_quantity
        if modifiers:
            instance.modifiers.set(modifiers)
        else:
            instance.modifiers.clear()  # Clear modifiers if none are provided

        instance.save()

        # Update the total price of the Order
        order = instance.order
        order.total_price = price
        order.delivery_location = self.__get_location(validated_data)
        order.save(update_fields=["total_price"])

        return instance


class OrderSerializer(serializers.ModelSerializer):
    # unique id that stripe generates and is passed from front end. Not required, if method is cash
    stripe_payment_method_id = serializers.CharField(write_only=True, required=False)
    customer_payment_method = serializers.ChoiceField(
        choices=PaymentMethodChoices.choices,
        write_only=True,
        required=False,
        default=PaymentMethodChoices.CASH,
    )
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid",
            "delivery_cost",
            "total_price",
            "delivery_location",
            "status",
            "customer_payment_method",
            "updated_at",
            "order_items",
            "stripe_payment_method_id",
        ]
        read_only_fields = list(
            set(fields)
            - {
                "stripe_payment_method_id",
                "customer_payment_method",
            }
        )

    @transaction.atomic
    def create(self, validated_data):
        """This method is for placing an order by changing status from cart to placed"""
        organization = get_organization(self.context["request"])

        try:
            # find existing order in cart
            order = Order.objects.filter(
                organization=organization,
                user=self.context["request"].user,
                status=OrderStatusChoices.CART,
            ).first()

        except Order.DoesNotExist:
            raise serializers.ValidationError("No active cart found.")

        for order_item in order.items.filter():
            item = order_item.item
            if (
                item.quantity < order_item.quantity
            ):  # Check for sufficient item quantity
                raise serializers.ValidationError(
                    "Insufficient quantity for item {item.name}"
                )
            item.quantity -= (
                order_item.quantity
            )  # Update item quantity in stock before placing order
            item.save(update_fields=["quantity"])

        # create transaction instance for given order
        customer_transaction = Transaction.objects.create(
            order=order,
            amount=order.total_price + order.delivery_cost,
            method=customer_payment_method,
        )

        customer_payment_method = validated_data.get("customer_payment_method")
        # Make stripe payment if option is card
        if customer_payment_method == PaymentMethodChoices.CARD:
            stripe_payment_method_id = validated_data.pop("stripe_payment_method_id")
            # call create_payment function written for making payment
            stripe_intent = create_payment(
                order.total_price + order.delivery_cost, stripe_payment_method_id
            )
            # Store stripe payment record
            customer_transaction.digital_transaction_id = stripe_intent.id

        # Update customer transaction information after successful payment
        customer_transaction.payment_method = customer_payment_method
        customer_transaction.payment_status = PaymentStatusChoices.SUCCESSFUL
        customer_transaction.save(
            update_fields=["digital_transaction_id", "payment_method", "payment_status"]
        )
        # Place the order
        order.status = OrderStatusChoices.PLACED
        order.save(update_fields=["status"])

        return {"order": order, "client_secret": stripe_intent.client_secret}
