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
    types = CategoryTypeSerializer()

    class Meta:
        model = Category
        fields = ("guid", "thumbnail", "title", "title_uz", "title_ru", "types")

    def create(self, validated_data):
        types = validated_data.pop("types")
        obj = Category.objects.create(**validated_data)
        for type_ in types:
            CategoryType.objects.create(**type_, category=obj)
        return obj


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

    # def get_types(self, obj):
    #     return obj.check_if_subscribed

    
class CategoryTestSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = CategoryType
        fields = ("guid", "price", "days", "category", )