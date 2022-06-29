from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...book.serializers.book import BookHelperSerializer
from ..models.book import Book
from ..models.favourite import Favourite

User = get_user_model()


class FavouriteCreateSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )

    def validate(self, attrs):
        self._errors = {}
        book = attrs.get("book")
        user = self.context["request"].user
        qs = Favourite.objects.filter(owner=user, book=book)
        if qs.exists():
            self._errors[
                "favourite error"
            ] = "This book already exists in your favourite list"

        if self.errors:
            raise serializers.ValidationError(self._errors)
        return attrs


class FavouriteListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Favourite
        fields = (
            "guid",
            "book",
            "rating",
        )

    def to_representation(self, instance):
        self.fields["book"] = BookHelperSerializer()
        return super().to_representation(instance)
