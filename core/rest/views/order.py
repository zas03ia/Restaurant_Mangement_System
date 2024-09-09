from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.rest.serializers.order import OrderSerializer, OrderItemSerializer
from order.models import Order, OrderItem
from order.choices import OrderStatusChoices
from shared.utils import get_organization


class PastOrdersListView(ListAPIView):
    """This view ia for getting a list of past orders"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return orders that are not in cart
        """
        organization = get_organization(self.request)
        try:
            orders = Order.objects.filter(
                organization=organization,
                user=self.request.user,
                status__ne=OrderStatusChoices.CART,
            )
        except Order.DoesNotExist:
            raise Exception("Could not fetch orders")
        return orders


class PlaceOrderView(CreateAPIView):
    """This view is for placing order"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class CartDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return order that is in cart
        """
        organization = get_organization(self.request)
        try:
            cart = Order.objects.filter(
                organization=organization,
                user=self.request.user,
                status=OrderStatusChoices.CART,
            ).first()
        except Order.DoesNotExist:
            raise Exception("Could not fetch cart details")
        return cart


class OrderItemDetailView(CreateAPIView, RetrieveUpdateDestroyAPIView):

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    """
    This view is for adding, updating and removing items from cart
    """

    def get_object(self):
        orderItem_uid = self.request.query_params.get("order_item_uid")
        try:
            order_item = OrderItem.objects.get(
                order__user=self.request.user,
                order__organization=get_organization(self.request),
                uid=orderItem_uid,
            )
            return order_item
        except OrderItem.DoesNotExist:
            raise Exception("Could not fetch order item details")
