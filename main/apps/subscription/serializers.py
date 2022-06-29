from datetime import date, timedelta

from rest_framework import serializers

from ..category.models import Category, CategoryType
from ..category.serializers import CategoryHelperSerializer
from .models import Subscription


class SubscriptionListSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    begin_date = serializers.DateField()
    end_date = serializers.DateField()
    price = serializers.CharField()
    active = serializers.CharField()

    def to_representation(self, instance):
        self.fields["category"] = CategoryHelperSerializer()
        return super(SubscriptionListSerializer, self).to_representation(
            instance,
        )


class SubscriptionCreateSerializer(serializers.Serializer):
    category = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Category.objects.all(),
    )
    category_type = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=CategoryType.objects.all(),
    )

    def validate(self, attrs):
        if self.context["request"].method == "POST":
            self._errors = {}

            category = attrs.get("category")
            category_type = attrs.get("category_type")
            owner = self.context["request"].user

            today = date.today()

            # TODO: add cronjob to check if active subscription exists
            subscription_obj = Subscription.objects.filter(
                category=category,
                owner=owner,
                active=True,
                end_date__gte=today,
            )
            if subscription_obj.exists():
                day = subscription_obj[0].end_date + timedelta(days=1)
                self._errors.update(
                    {
                        "errors": dict(
                            message=f"Subscription for this category "
                            f"expires on "
                            f"{subscription_obj[0].end_date}, you can "
                            f"subscribe on {day}",
                        ),
                    },
                )

            if category_type.category != category:
                self._errors.update(
                    {
                        "errors": dict(
                            message="category type's category does not match"
                            "with actual category",
                        ),
                    },
                )
            if category_type.price > owner.check_balance:
                msg = "Insufficient balance"
                self._errors.update(
                    {
                        "errors": dict(
                            message=f"{msg}: {owner.check_balance}",
                        ),
                    },
                )
            if self._errors:
                raise serializers.ValidationError(self._errors)
        return attrs
