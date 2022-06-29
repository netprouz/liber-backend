from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.rate import RateManager

User = get_user_model()


class RATEChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Rate(BaseModel):
    point = models.IntegerField(
        choices=RATEChoices.choices,
        default=RATEChoices.THREE,
    )
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="rates"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rates",
    )
    objects = RateManager()

    def update_rate(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta(BaseMeta):
        unique_together = ["owner", "book"]
        verbose_name = _("Rate")
        verbose_name_plural = _("Rates")

    def __str__(self) -> str:
        return f"{self.point}"
