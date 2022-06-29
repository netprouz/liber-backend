from rest_framework import serializers

from ..account.models.user_book import UserBook
from ..book.models.book import Book
from ..book.models.book_type import BookType, TYPEChoices
from ..book.serializers.book import BookHelperSerializer
from .models import Order, PAYMENTTypeChoices


class BookTypeHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = (
            "guid",
            "book_type",
            "price",
        )


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "guid",
            "book",
            "book_type",
            "payment_type",
            "order_number",
            "total_price",
            "quantity",
            "phone_number",
            "full_name",
        )

    def to_representation(self, instance):
        self.fields["book"] = BookHelperSerializer()
        self.fields["book_type"] = BookTypeHelperSerializer()
        return super().to_representation(instance)


class OrderCreateSerializer(serializers.Serializer):
    book = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=Book.objects.all(),
    )
    book_type = serializers.SlugRelatedField(
        slug_field="guid",
        queryset=BookType.objects.all(),
    )
    payment_type = serializers.ChoiceField(choices=PAYMENTTypeChoices.choices)
    quantity = serializers.IntegerField(default=1)
    phone_number = serializers.CharField(required=False, max_length=15)
    full_name = serializers.CharField(required=False)

    def validate(self, attrs):
        self._errors = {}
        book_type = attrs.get("book_type")
        book = attrs.get("book")
        payment_type = attrs.get("payment_type")
        quantity = attrs.get("quantity", 1)
        user = self.context["request"].user

        if UserBook.objects.filter(
            book=book,
            book_type=book_type.book_type,
            owner=user,
        ).exists():
            msg = "A book cannot be bought more than once"
            self._errors.update(
                {
                    "errors": dict(
                        message=msg,
                    ),
                },
            )

        if book_type.book != book:
            msg = "this book type does not belong to the given book"
            self._errors.update(
                {
                    "errors": dict(
                        message=msg,
                    ),
                },
            )
        """
        validation rules:
        Note:
        there are only two types of payment types
            1. online -> takes money from user balance
            2. cash -> paid in cash
        if during the ordering process, payment type is online:
            I. if book type hardcopy (paper)
                I. book_type_price * quantity (quantity is considered)
            II. if price > user_balance
                :raise error (insufficient balance)
            III. you can buy any of the types of the book
                It means you can buy (epub, audio and hardcopy) book
            IV. if user wants to buy epub or audio format of a book.
                quantity is not considered. it is not taken into account
                quantity only works with hardcopy of a book
        if during the ordering process, payment type is cash:
                    user cannot purchase epub and audio format of a book
                    with cash, you can purchase only hardcopy of a book
        """
        if payment_type == PAYMENTTypeChoices.ONLINE:
            price = book_type.price
            if book_type.book_type == TYPEChoices.PAPER:
                price *= quantity
            if price > user.check_balance:
                msg = "Insufficient balance"
                self._errors.update(
                    {
                        "errors": dict(
                            message=f"{msg}: {user.check_balance}",
                        ),
                    },
                )
        if payment_type == PAYMENTTypeChoices.CASH:
            if (book_type.book_type == TYPEChoices.ONLINE) or (
                book_type.book_type == TYPEChoices.AUDIO
            ):
                msg = "PDF and Audio formats can only be purchased online"

                self._errors.update(
                    {
                        "errors": dict(
                            message=msg,
                        ),
                    },
                )
        if self._errors:
            raise serializers.ValidationError(self._errors)

        return attrs


class CompleteOrderSerializer(serializers.Serializer):
    is_paid = serializers.BooleanField(default=False)
    is_completed = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.is_paid = validated_data.get("is_paid", instance.is_paid)
        instance.is_completed = validated_data.get(
            "is_completed",
            instance.is_completed,
        )
        instance.save()
        return validated_data
