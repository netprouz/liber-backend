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
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderListSerializer
    filterset_class = OrderFilterSet

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


order_list_api_view = OrderListAPIView.as_view()

from ...common.permissions import CreatePermission


class AllOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderListSerializer
    filterset_class = OrderFilterSet
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, CreatePermission]

all_order_api_view = AllOrderListAPIView.as_view()


class OrderCompleteAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = CompleteOrderSerializer
    lookup_field = "guid"


oder_complete_api_view = OrderCompleteAPIView.as_view()


