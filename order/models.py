from django.db import models
from shared.models import BaseModel
from .choices import OrderStatusChoices
from accountio.models import Organization, Location
from core.models import User
from menu.models import Item, Modifier


# Create your models here.
class Order(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="orders"
    )
    delivery_cost = models.IntegerField(default=40)
    total_price = models.IntegerField(default=0)
    delivery_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.CART,
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=1)
    modifiers = models.ManyToManyField(Modifier, related_name="order_items")

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
