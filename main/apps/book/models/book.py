import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.book import BookManager
from autoslug import AutoSlugField


def upload_book_cover(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"book/{filename}"
    

User = get_user_model()
ONLINE = settings.ONLINE
AUDIO = settings.AUDIO
PAPER = settings.PAPER


class Book(BaseModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', null=True)
    author = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(blank=True, upload_to=upload_book_cover)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="books"
    )
    language = models.CharField(max_length=255, blank=True)
    hardcover = models.PositiveIntegerField()
    short_description = models.TextField(blank=True)
    published_date = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    objects = BookManager()
    

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def update_with_types(self, data):
        book_types = data.pop("book_types")
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        self.types.all().delete()
        self.types.create_book_type(book_types)

    @classmethod
    def return_online_books(self):
        from ..models.content import Content

        return Content.objects.filter(book=self.id, book_type=ONLINE)
        
    @classmethod
    def return_audio_books(self):
        from ..models.content import Content

        return Content.objects.filter(book=self.id, book_type=AUDIO)

    # def set_purchased_book_types_true(self, user):
    #     from ...account.models.user_book import UserBook

    #     type_list = []
    #     for book_type in self.types.all():
    #         is_purchased = False
    #         reference = ""

    #         qs = UserBook.objects.filter(
    #             book=self, owner=user, book_type=book_type.book_type
    #         )
    #         if qs.exists():
    #             is_purchased = True
    #             reference = qs.first().guid
    #         data = dict(
    #             guid=book_type.guid,
    #             book_type=book_type.book_type,
    #             price=book_type.price,
    #             is_purchased=is_purchased,
    #             reference=reference,
    #         )
    #         type_list.append(data)
    #     return type_list

    class Meta(BaseMeta):
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self) -> str:
        return self.title
