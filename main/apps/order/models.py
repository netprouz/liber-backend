from django.contrib.auth import get_user_model
from django.db import models

from ..common.models import BaseModel
from .managers import OrderManager

User = get_user_model()


class PAYMENTTypeChoices(models.TextChoices):
    CASH = "cash"
    ONLINE = "online"


class Order(BaseModel):
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENTTypeChoices.choices,
    )
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    book_type = models.ForeignKey(
        "book.BookType",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    phone_number = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    order_number = models.CharField(unique=True, max_length=50)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    objects = OrderManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.guid}"
