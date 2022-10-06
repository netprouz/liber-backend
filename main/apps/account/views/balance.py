from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..models.balance import Balance
from ..serializers.balance import BalanceCreateSerializer

from rest_framework_simplejwt import authentication
from rest_framework import permissions


class BalanceCreateAPIView(generics.CreateAPIView):
    model = Balance
    serializer_class = BalanceCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return self.model.objects.create_balance_instance(
            self.request.user,
            serializer.validated_data,
        )


balance_create_api_view = BalanceCreateAPIView.as_view()


class BalanceDeleteAPIView(generics.DestroyAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, DeletePersonalObjectPermission]
    lookup_field = "guid"


balance_delete_api_view = BalanceDeleteAPIView.as_view()
