from rest_framework import generics

from ..filters.order import OrderFilterSet
from ..models import Order
from ..serializers import CompleteOrderSerializer  # noqa
from ..serializers import OrderCreateSerializer, OrderListSerializer

from rest_framework_simplejwt import authentication
from rest_framework import permissions


class OrderCreateAPIView(generics.CreateAPIView):
    model = Order
    serializer_class = OrderCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        return self.model.objects.create_order_instance(
            self.request.user, serializer.validated_data
        )


order_create_api_view = OrderCreateAPIView.as_view()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    filterset_class = OrderFilterSet

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


oder_list_api_view = OrderListAPIView.as_view()


class OrderCompleteAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = CompleteOrderSerializer
    lookup_field = "guid"


oder_complete_api_view = OrderCompleteAPIView.as_view()


