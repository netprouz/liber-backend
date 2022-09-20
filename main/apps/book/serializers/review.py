from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...account.serializers.user import UserSerializer
from ..models.book import Book
from ..models.rate import Rate, RATEChoices

User = get_user_model()


class ReviewCreateSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    point = serializers.ChoiceField(
        choices=RATEChoices.choices,
    )
    title = serializers.CharField()
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )

    def validate(self, attrs):
        self._errors = {}
        book = attrs.get("book")
        user = self.context["request"].user
        qs = Rate.objects.filter(owner=user, book=book)
        if qs.exists():
            self._errors["rating error"] = "You have rated this book already"

        if self.errors:
            raise serializers.ValidationError(self._errors)
        return attrs


class ReviewListSerializer(serializers.Serializer):
    class TimestampField(serializers.Field):
        def to_representation(self, value):
            return value.date()

    guid = serializers.UUIDField(read_only=True)
    point = serializers.ChoiceField(
        choices=RATEChoices.choices,
    )
    title = serializers.CharField()
    created_at = TimestampField()
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    def to_representation(self, instance):
        self.fields["owner"] = UserSerializer()
        return super(ReviewListSerializer, self).to_representation(instance)
