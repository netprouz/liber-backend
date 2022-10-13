from email.policy import default
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
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    token_for_register = models.TextField(null=True,blank=True)
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

    
    def token_save(self,token,subscription_id):

        subscription = Subscription.objects.get(id=subscription_id)
        subscription.token_for_register = token

        subscription.save()