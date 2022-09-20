from email.mime import audio
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
    # published_date = serializers.DateField(format="%Y", required=False)
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
            "publisher",
            "isbn",
            "short_description",
            'short_description_uz',
            'short_description_ru',
            "published_date",
            "types",
        )

    # def validate(self, attrs):
    #     self._errors = {}
    #     types = attrs.get("types")
    #     res = []
    #     for type_ in types:
    #         if type_.get("types") in res:
    #             self._errors[type_.get("types")] = dict(
    #                 message=_(f"{type_['types']} cannot be duplicate")
    #             )
    #         else:
    #             res.append(type_.get("types"))
    #     if self._errors:
    #         raise serializers.ValidationError(self._errors)

    #     return attrs

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
            "publisher",
            "isbn",
            'short_description',
            'short_description_uz',
            'short_description_ru',
            'published_date',
            'created_at',
            
        )


class BookListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    category_uz = serializers.ReadOnlyField(source='category.title_uz')
    category_ru = serializers.ReadOnlyField(source='category.title_ru')
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
            'category_uz',
            'category_ru',
            'language',
            "publisher",
            "isbn",
            'short_description',
            'short_description_uz',
            'short_description_ru',
            'published_date',
            'created_at',
            'types',
            
        )



class BookDetailSerializer(serializers.ModelSerializer):
    # types = serializers.SerializerMethodField()
    # view = serializers.IntegerField()
    types = BookTypeSerializer(read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)
    # published_date = serializers.DateField(format="%Y", input_formats=['%Y'])
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
            "publisher",
            "isbn",
            "short_description",
            'short_description_uz',
            'short_description_ru',
            "published_date",
            "reviews",
            # "view",
            "types",
            "reviews",
            "created_at"
        )

    def __init__(self, *args, **kwargs):
        super(BookDetailSerializer, self).__init__(*args, **kwargs)
        self.user = None
        if self.context.get("request"):
            self.user = self.context["request"].user

    def to_representation(self, instance):
        self.fields["category"] = CategoryHelperSerializer()
        return super().to_representation(instance)

    # def get_types(self, obj):
    #     return obj.set_purchased_book_types_true(self.user)


class BookUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="guid", queryset=Category.objects.all()
    )
    types = BookTypeSerializer(many=True)
    # published_date = serializers.DateField(format="%Y", required=False)
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
            "publisher",
            "isbn",
            "short_description",
            'short_description_uz',
            'short_description_ru',
            "published_date",
            "types",
        )


    def update(self, instance, validated_data):
        types_data = validated_data.pop('types')
        types = (instance.types).all()
        types = list(types)
        instance.title = validated_data.get('title', instance.title)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.short_description_uz = validated_data.get('short_description_uz', instance.short_description_uz)
        instance.short_description_ru = validated_data.get('short_description_ru', instance.short_description_ru)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.language = validated_data.get('language', instance.language)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.hardcover = validated_data.get('hardcover', instance.hardcover)
        instance.save()

        for type_data in types_data:
            type = types.pop(0)
            type.book_type = type_data.get('book_type', type.book_type)
            type.price = type_data.get('price', type.price)
            type.save()
        return instance


class BookPublishedDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['published_date']


# class AudiouploadSerializer( serializers.Serializer ):
#     audio_upload = serializers.ListField(
#                        child=serializers.FileField( max_length=100000,
#                                          allow_empty_file=False,
#                                          use_url=False )
#                                 )
#     def create(self, validated_data):
#         # blogs=Blogs.objects.latest('created_at')
#         audio_upload=validated_data.pop('audio_upload')
#         for audio in audio_upload:
#             aud=Book.objects.create(audio_upload=audio, **validated_data)
#         return aud