from django.db import models


class PaymentStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    FAILED = "failed", "Failed"
    SUCCESSFUL = "successful", "Successful"


class PaymentMethodChoices(models.TextChoices):
    CARD = "card", "Card"
    CASH = "cash", "Cash on delivery"
