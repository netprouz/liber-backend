from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.favourite import FavouriteManager
from main.apps.book.models.review import Review
from main.apps.book.models.rate import Rate

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


    def get_review(self, *args, **kwargs):
        res = Review.objects.filter(owner=self.id).count()
        return {"review":res}

    def get_rate(self, *args, **kwargs):
        rate = Rate.objects.filter(owner=self.id).count()
        return {"rate":rate}


    def update_rate(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta(BaseMeta):
        verbose_name = _("Favourite")
        verbose_name_plural = _("Favourite")

    def __str__(self) -> str:
        return f"{self.id}"
