import os
from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ...common.models import BaseModel
from ..managers.user import UserManager


def upload_profile_images(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"profile/{filename}"


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class GenderChoices(models.TextChoices):
        MALE = "male"
        FEMALE = "female"

    # phone_number = models.CharField(
    #     _("Phone number"),
    #     max_length=15,
    #     unique=True,
    #     error_messages={
    #         "unique": _(
    #             "User with this phone number already exists.",
    #         )
    #     },
    #     blank=False,
    #     null=False,
    # )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    unique_identifier = models.PositiveIntegerField(unique=True, blank=True, null=True)
    # last_name = models.CharField(_("last name"), max_length=150, blank=True)
    activating_code = models.CharField(max_length=6, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=upload_profile_images,
        blank=True,
    )
    # email = models.EmailField(_("email address"), blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    otp = models.CharField(max_length=6, null=True)
    is_virified = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    is_moderator = models.BooleanField(_("moderator status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=15,
        default=GenderChoices.MALE,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    objects = UserManager()

    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        ordering = ("-id",)
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name}"

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_profile(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    def create_balance(self, amount):
        self.balances.create(amount=amount)

    @property
    def check_balance(self):
        return (
            self.balances.aggregate(balance=Coalesce(Sum("amount"), Decimal(0)))
                .get("balance")
        )

    def __str__(self):
        return f"{self.username} {self.first_name}"
