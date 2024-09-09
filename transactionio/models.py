from django.db import models
from shared.models import BaseModel
from order.models import Order
from .choices import PaymentStatusChoices, PaymentMethodChoices

# Create your models here.


class Transaction(BaseModel):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="transaction"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CASH,
    )
    payment_status = models.CharField(
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    digital_transaction_id = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id} for Order {self.order.id}"
