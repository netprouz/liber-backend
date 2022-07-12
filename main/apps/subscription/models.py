from django.contrib.auth import get_user_model
from django.db import models

from ..common.models import BaseModel
from .managers import SubscriptionManager

User = get_user_model()


# TODO: check if there is existing subscription that expire today
class Subscription(BaseModel):
    category = models.ForeignKey(
        "category.Category",
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    category_type = models.ForeignKey(
        "category.CategoryType",
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )

    begin_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    objects = SubscriptionManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.guid}"

    def disable_instance(self):
        self.active = False
        self.save()
