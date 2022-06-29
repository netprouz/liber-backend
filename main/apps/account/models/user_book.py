import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

online = settings.ONLINE
audio = settings.AUDIO

permanent = settings.PERMANENT
temporary = settings.TEMPORARY


class BOOKTYPEChoices(models.TextChoices):
    ONLINE = online, _(online)
    AUDIO = audio, _(audio)


class BOOKSTATEChoices(models.TextChoices):
    PERMANENT = permanent, _(permanent)
    TEMPORARY = temporary, _(temporary)


class UserBook(models.Model):
    category = models.ForeignKey(
        "category.Category",
        on_delete=models.CASCADE,
        related_name="customer_books",
    )
    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="customer_books"
    )
    owner = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="purchased_books",
    )
    book_type = models.CharField(
        max_length=20,
        choices=BOOKTYPEChoices.choices,
    )
    state = models.CharField(
        max_length=15,
        choices=BOOKSTATEChoices.choices,
    )
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "User Book"
        verbose_name_plural = "User Books"

    def __str__(self) -> str:
        return f"{self.guid}"
