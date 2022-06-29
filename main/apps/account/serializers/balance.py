from rest_framework import serializers


class BalanceCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
