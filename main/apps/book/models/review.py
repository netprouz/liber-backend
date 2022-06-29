from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.review import ReviewManager

User = get_user_model()


class Review(BaseModel):
    title = models.TextField()
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="reviews"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    objects = ReviewManager()

    def update_rate(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta(BaseMeta):
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self) -> str:
        return f"{self.id}"
