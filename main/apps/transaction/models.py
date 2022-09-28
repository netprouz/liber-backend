from django.db import models
from ..common.models import BaseModel

from django.contrib.auth import get_user_model

User = get_user_model()


class TRANSACTIONTYPECHOICES(models.TextChoices):
    PAYME = "payme"
    CLICK = "click"


class TRANSACTIONSTATUS(models.TextChoices):
    NEW = "new"
    PAID = "paid"
    CANCELED = "canceled"


class Transaction(BaseModel):
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTIONTYPECHOICES.choices,
    )
    status = models.CharField(
        max_length=10,
        choices=TRANSACTIONSTATUS.choices,
        default=TRANSACTIONSTATUS.NEW
    )
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.guid)
