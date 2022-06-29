from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.favourite import FavouriteManager

User = get_user_model()


class Favourite(BaseModel):
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="favourites"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favourites",
    )
    objects = FavouriteManager()

    def update_rate(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta(BaseMeta):
        verbose_name = _("Favourite")
        verbose_name_plural = _("Favourite")

    def __str__(self) -> str:
        return f"{self.id}"
