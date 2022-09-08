from rest_framework import serializers

from .models import Category, CategoryType


class CategoryHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("guid", "title", "thumbnail")


class CategoryTypeSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    days = serializers.IntegerField(required=True)
    price = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        required=True,
    )


class CategoryModelSerializer(serializers.ModelSerializer):
    types = CategoryTypeSerializer(many=True, write_only=True)

    class Meta:
        model = Category
        fields = ("guid", "thumbnail", "title", "title_uz", "title_ru", "types")


    def create(self, validated_data):
        types_data = validated_data.pop("types")
        obj = Category.objects.create(**validated_data)
        for type_ in types_data:
            CategoryType.objects.create(**type_, category=obj)
        return obj


class CategoryUpdateSerializer(serializers.ModelSerializer):
    category_types = CategoryTypeSerializer(many=True)

    class Meta:
        model = Category
        fields = ("guid", "thumbnail", "title", "title_uz", "title_ru", "category_types")


    def update(self, instance, validated_data):
        albums_data = validated_data.pop('category_types')
        albums = (instance.category_types).all()
        albums = list(albums)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        for album_data in albums_data:
            album = albums.pop(0)
            album.days = album_data.get('days', album.days)
            album.price = album_data.get('price', album.price)
            album.save()
        return instance


class CategoryListSerializer(serializers.ModelSerializer):
    category_types = CategoryTypeSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "guid", 
            "thumbnail", 
            "title", 
            "title_uz", 
            "title_ru", 
            "category_types"
            )

    def get_category_types(self, obj):
        return obj.check_if_subscribed

    
class CategoryTestSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = CategoryType
        fields = ("guid", "price", "days", "category", )