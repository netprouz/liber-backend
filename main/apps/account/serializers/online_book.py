from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...book.serializers.book import BookHelperSerializer
from ..models.online_book import OnlineBook

User = get_user_model()


class OnlineBookSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = OnlineBook
        fields = (
            "guid",
            "book",
            "book_type",
            "rating",
        )

    def to_representation(self, instance):
        self.fields["book"] = BookHelperSerializer()
        return super().to_representation(instance)


class ContentListSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    title = serializers.CharField()
    book_type = serializers.CharField()


class BookListSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    title = serializers.CharField()
    author = serializers.CharField()
    thumbnail = serializers.ImageField()
    contents = serializers.SerializerMethodField()

    def get_contents(self, obj):
        return ContentListSerializer(obj.return_online_books(), many=True).data


class OnlineBookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineBook
        fields = ("guid", "book")

    def to_representation(self, instance):
        self.fields["book"] = BookListSerializer()
        return super(OnlineBookDetailSerializer, self).to_representation(
            instance,
        )
