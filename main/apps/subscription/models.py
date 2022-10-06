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


class SubscriptionTransaction(models.Model):
    """
    Payme uchun Transaction model
    """
    PROCESS = 0
    PAID = 1
    FAILED = 2
    STATUS = (
        (PROCESS, 'processing'),
        (PAID, 'paid'),
        (FAILED, 'failed'),
    )

    trans_id = models.CharField(max_length=255)
    request_id = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    account = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, default=PROCESS, choices=STATUS)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now=True)



    


    def create_transaction(self, trans_id, request_id, amount, account, status):
        SubscriptionTransaction.objects.create(
            trans_id=trans_id,
            request_id=request_id,
            amount=amount / 100,
            account=account,
            status=status
        )

    def update_transaction(self, trans_id, status):
        trans = SubscriptionTransaction.objects.get(trans_id=trans_id)
        trans.status = status
        trans.save()
    
    