from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce

ONLINE = settings.ONLINE


class OnlineBookManager(models.Manager):
    def get_queryset(self):
        return (
            super(OnlineBookManager, self)
            .get_queryset()
            .filter(
                book_type=ONLINE,
            )
        )

    def filter_with_rates(self):
        return self.annotate(
            rating=Coalesce(
                Avg("book__rates__point"),
                float(0),
            )
        )
