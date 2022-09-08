from email.policy import default
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...category.models import Category
from ...category.serializers import CategoryHelperSerializer
from ..models.book import Book
from ..models.book_type import BookType
from ..serializers.book_type import BookTypeSerializer
from ..serializers.review import ReviewListSerializer


class BookHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("guid", "title", "author", "thumbnail")


class BookCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="guid", queryset=Category.objects.all()
    )
    types = BookTypeSerializer(many=True, write_only=True)
    published_date = serializers.DateField(format="%Y", required=False)
    class Meta:
        model = Book
        fields = (
            "guid",
            "title",
            'slug',
            "author",
            "thumbnail",
            "category",
            "language",
            "hardcover",
            "short_description",
            'short_description_uz',
            'short_description_ru',
            "published_date",
            "types",
        )

    def validate(self, attrs):
        self._errors = {}
        types = attrs.get("types")
        res = []
        for type_ in types:
            if type_.get("types") in res:
                self._errors[type_.get("types")] = dict(
                    message=_(f"{type_['types']} cannot be duplicate")
                )
            else:
                res.append(type_.get("types"))
        if self._errors:
            raise serializers.ValidationError(self._errors)

        return attrs

    def create(self, validated_data):
        book_types = validated_data.pop("types")
        book_obj = Book.objects.create(**validated_data)
        for book_type in book_types:
            BookType.objects.create(**book_type, book=book_obj)
        return book_obj


class BookListForBookTypeSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    created_at = serializers.DateTimeField('%Y-%m-%d, %X' )
    rating = serializers.IntegerField(default=0)
    class Meta:
        model = Book
        fields = (
            'guid',
            'title',
            'slug',
            'author',
            'thumbnail',
            'rating',
            'category',
            'language',
            'short_description',
            'short_description_uz',
            'short_description_ru',
            'published_date',
            'created_at',
            
        )


class BookListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    created_at = serializers.DateTimeField('%Y-%m-%d, %X' )
    types = BookTypeSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(default=0)
    # published_date = serializers.DateField(format="%Y", input_formats=['%Y'])
    class Meta:
        model = Book
        fields = (
            'guid',
            'title',
            'slug',
            'author',
            'thumbnail',
            'rating',
            'category',
            'language',
            'short_description',
            'short_description_uz',
            'short_description_ru',
            'published_date',
            'created_at',
            'types',
            
        )



class BookDetailSerializer(serializers.ModelSerializer):
    types = serializers.SerializerMethodField()
    view = serializers.IntegerField()
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            "guid",
            "title",
            "author",
            "thumbnail",
            "category",
            "language",
            "hardcover",
            "short_description",
            'short_description_uz',
            'short_description_ru',
            "published_date",
            "reviews",
            "view",
            "types",
            "reviews",
        )

    def __init__(self, *args, **kwargs):
        super(BookDetailSerializer, self).__init__(*args, **kwargs)
        self.user = None
        if self.context.get("request"):
            self.user = self.context["request"].user

    def to_representation(self, instance):
        self.fields["category"] = CategoryHelperSerializer()
        return super().to_representation(instance)

    def get_types(self, obj):
        return obj.set_purchased_book_types_true(self.user)
