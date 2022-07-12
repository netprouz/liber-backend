from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from ..models.book import Book
from ..models.content import BOOKTYPEChoices


class ContentCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField()
    book_type = serializers.ChoiceField(
        choices=BOOKTYPEChoices.choices,
    )
    body = serializers.FileField(validators=[FileExtensionValidator(["mp3", "epub"])])
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )


class ContentListSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    title = serializers.CharField()
    book_type = serializers.CharField()


class ContentDetailSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    title = serializers.CharField()
    book_type = serializers.CharField()
    body = serializers.FileField()
    created_at = serializers.DateTimeField()
