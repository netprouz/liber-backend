from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseModel
from ..managers.balance import BalanceManager



class Balance(BaseModel):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    owner = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="balances",
    )
    objects = BalanceManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return f"{self.guid}"
