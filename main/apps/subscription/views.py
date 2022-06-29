from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionCreateSerializer  # noqa
from .serializers import SubscriptionListSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    model = Subscription
    serializer_class = SubscriptionCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_subscription_instance(
            self.request.user,
            serializer.validated_data,
        )


subscription_create_api_view = SubscriptionCreateAPIView.as_view()


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    filterset_fields = ["category", "active"]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


subscription_list_api_view = SubscriptionListAPIView.as_view()


# TODO: remove this function after cronjob has been installed
class SubscriptionAPIView(APIView):
    def get(self, request):
        from .utils import disable_active_subscriptions

        disable_active_subscriptions()
        return Response(200)


subscription_view = SubscriptionAPIView.as_view()
