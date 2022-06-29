from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseModel

User = get_user_model()


class View(BaseModel):
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="views"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="views",
    )

    def update_view(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")

    def __str__(self) -> str:
        return f"{self.id}"
