from django.db import models
from ..common.models import BaseModel

from django.contrib.auth import get_user_model

User = get_user_model()


class TRANSACTIONTYPECHOICES(models.TextChoices):
    PAYME = "payme"
    CLICK = "click"


class TRANSACTIONSTATUS(models.TextChoices):
    NEW = "new"
    VERIFIED = "verified"
    PAID = "paid"
    CANCELED = "canceled"


class Transaction(BaseModel):
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_external_id = models.CharField(max_length=30, blank=True, default="")
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
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

    def verify(self):
        self.status = TRANSACTIONSTATUS.VERIFIED
        self.is_verified = True
        self.save()

    def make_payment(self):
        self.status = TRANSACTIONSTATUS.PAID
        self.is_paid = True
        self.save()

    def cancel(self):
        self.status = TRANSACTIONSTATUS.CANCELED
        self.is_canceled = True
        self.is_paid = False
        self.save()

    def __str__(self):
        return str(self.guid)
