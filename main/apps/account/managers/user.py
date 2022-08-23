from decimal import Decimal

from django.contrib.auth.base_user import BaseUserManager
from django.db.models import DecimalField, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce

from ...common.managers import BaseManager


class UserManager(BaseUserManager, BaseManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given phone number must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_moderator(self, username, password, **extra_fields):
        extra_fields.setdefault("is_moderator", True)

        if extra_fields.get("is_moderator") is not True:
            raise ValueError("Moderator must have is_moderator=True.")

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_moderator", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def get_or_create(self, username, password, **kwargs):
        try:
            instance = self.model.objects.get(username=username)
            return instance, False
        except self.model.DoesNotExist:
            instance = self.model.objects.create_user(
                username=username, password=password, **kwargs
            )
            return instance, True

    def filter_details(self):
        from ..models.balance import Balance

        output = DecimalField(max_digits=20, decimal_places=2)

        target_query = Balance.objects.filter(
            owner=OuterRef("pk"),
        )
        target_query = target_query.order_by()
        target_query = target_query.annotate(
            total=Coalesce(
                Sum("amount"),
                Decimal(0),
            ),
        )
        target_query = target_query.values("total")
        target_query.query.group_by = []

        users = self.annotate(
            balance=Subquery(
                target_query[:1],
                output_field=output,
            )
        )
        users = users.prefetch_related("orders", "transactions")
        return users
