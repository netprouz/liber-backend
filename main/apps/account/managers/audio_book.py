from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce

AUDIO = settings.AUDIO


class AudionBookManager(models.Manager):
    def get_queryset(self):
        return (
            super(AudionBookManager, self)
            .get_queryset()
            .filter(
                book_type=AUDIO,
            )
        )

    def filter_with_rates(self):
        return self.annotate(
            rating=Coalesce(
                Avg("book__rates__point"),
                float(0),
            )
        )
