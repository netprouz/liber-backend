import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ..common.models import BaseMeta, BaseModel
from .managers.category import CategoryManager
from .managers.category_type import CategoryTypeManager

User = get_user_model()


def upload_category_images(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"category/{filename}"

import json

class Category(BaseModel):
    thumbnail = models.ImageField(upload_to=upload_category_images)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    objects = CategoryManager()

    class Meta(BaseMeta):
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def update_category(self, data):
        types = data.pop("types")
        for field, value in data.items():
            setattr(self, field, value)
        self.types.all().delete()
        self.types.create_category_type_instance(types)
        self.save()

    def __str__(self) -> str:
        return self.title

    # @property
    # def check_if_subscribed(self):
    #     from ..subscription.models import Subscription

    #     type_lst = []
    #     for _type in self.types.all():
    #         print(self.types.all())
    #         is_subscribed = False
    #         if Subscription.objects.filter(category=self, category_type=_type, active=True).exists():
    #             is_subscribed = True
    #         type_lst.append(dict(
    #             guid=_type.guid,
    #             days=_type.days,
    #             price=_type.price,
    #             is_subscribed=is_subscribed
    #         ))
    #         print(json.dumps(type_lst))
    #     return type_lst


class CategoryType(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category_types",
    )
    price = models.DecimalField(max_digits=20, decimal_places=2)
    days = models.IntegerField(default=1)
    objects = CategoryTypeManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Category Type")
        verbose_name_plural = _("Category Types")

    def update_category_type(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    def __str__(self) -> str:
        return f"{self.guid}"
