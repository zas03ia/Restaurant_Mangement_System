from django.db import models


class OrderStatusChoices(models.TextChoices):
    CART = "cart", "Cart"
    PLACED = "placed", "Placed"
    ACCEPTED = "accepted", "Accepted"
    PREPARING = "preparing", "Preparing"
    RIDER = "rider", "Rider on the way"
    RECEIVED = "received", "Received"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
