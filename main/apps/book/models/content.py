import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseModel
from ..managers.content import ContentManager

User = get_user_model()

online = settings.ONLINE
audio = settings.AUDIO


def upload_book_cover(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"content/{filename}"


class BOOKTYPEChoices(models.TextChoices):
    ONLINE = online, _(online)
    AUDIO = audio, _(audio)


class Content(BaseModel):
    title = models.CharField(max_length=255)
    book_type = models.CharField(
        max_length=20,
        choices=BOOKTYPEChoices.choices,
    )
    body = models.FileField(upload_to=upload_book_cover)
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="contents"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="book_contents",
    )
    objects = ContentManager()

    def update_content(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __str__(self) -> str:
        return self.title
