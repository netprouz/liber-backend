from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..models.balance import Balance
from ..serializers.balance import BalanceCreateSerializer


class BalanceCreateAPIView(generics.CreateAPIView):
    model = Balance
    serializer_class = BalanceCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_balance_instance(
            self.request.user,
            serializer.validated_data,
        )


balance_create_api_view = BalanceCreateAPIView.as_view()


class BalanceDeleteAPIView(generics.DestroyAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceCreateSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


balance_delete_api_view = BalanceDeleteAPIView.as_view()
