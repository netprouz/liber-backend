from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...account.serializers.user import UserSerializer
from ..models.book import Book

User = get_user_model()


class ReviewCreateSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )


class ReviewListSerializer(serializers.Serializer):
    class TimestampField(serializers.Field):
        def to_representation(self, value):
            return value.date()

    guid = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    created_at = TimestampField()
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    def to_representation(self, instance):
        self.fields["owner"] = UserSerializer()
        return super(ReviewListSerializer, self).to_representation(instance)
