from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...book.serializers.book import BookHelperSerializer
from ..models.book import Book
from ..models.recommendation import Recommendation

User = get_user_model()


class RecommendationCreateSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )


class RecommendationListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Recommendation
        fields = (
            "guid",
            "book",
            "rating",
        )

    def to_representation(self, instance):
        self.fields["book"] = BookHelperSerializer()
        return super().to_representation(instance)
