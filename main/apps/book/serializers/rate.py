from rest_framework import serializers

from ..models.book import Book
from ..models.rate import Rate, RATEChoices


class RateCreateUpdateSerializer(serializers.Serializer):
    point = serializers.ChoiceField(
        choices=RATEChoices.choices,
    )

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
