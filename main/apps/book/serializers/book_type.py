from rest_framework import serializers

from ..models.book_type import TYPEChoices


class BookTypeSerializer(serializers.Serializer):
    guid = serializers.UUIDField(required=False)
    book_type = serializers.ChoiceField(
        choices=TYPEChoices.choices, 
    )
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    thumbnail = serializers.URLField(required=False)
