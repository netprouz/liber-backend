from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from ..models.book import Book
from ..models.content import BOOKTYPEChoices, Content


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

from .book import BookListForBookTypeSerializer

class ContentListForBookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('guid', 'title', 'book_type', 'body')


class ContentListSerializer(serializers.ModelSerializer):
    book_image = serializers.ImageField(source="book.thumbnail", read_only=True)
    book_author = serializers.ReadOnlyField(source="book.author")
    class Meta:
        model = Content
        fields = (
            "guid",
            "title",
            "book_type",
            "body",
            "book_image",
            "book_author"
        )


class ContentDetailSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    title = serializers.CharField()
    book_type = serializers.CharField()
    body = serializers.FileField()
    created_at = serializers.DateTimeField()
