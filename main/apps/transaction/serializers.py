from rest_framework import serializers

from ..account.serializers.user import UserSerializer
from .models import TRANSACTIONTYPECHOICES, Transaction


class InitializePaymentSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(
        choices=TRANSACTIONTYPECHOICES.choices,
    )
    price = serializers.DecimalField(max_digits=20, decimal_places=2)


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "guid",
            "transaction_type",
            "is_verified",
            "is_paid",
            "is_canceled",
            "status",
            "transaction_external_id",
            "total_price",
            "comment",
            "owner",
            "created_at",
        )

    def to_representation(self, instance):
        self.fields["owner"] = UserSerializer()
        return super().to_representation(instance)
