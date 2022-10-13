from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.apps.category.models import CategoryType

from .models import Subscription
from .serializers import SubscriptionCreateSerializer  # noqa
from .serializers import SubscriptionListSerializer, SubscribeSerializer

from rest_framework_simplejwt import authentication
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SubscribeSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    model = Subscription
    serializer_class = SubscriptionCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return self.model.objects.create_subscription_instance(
            self.request.user,
            serializer.validated_data,
        )


subscription_create_api_view = SubscriptionCreateAPIView.as_view()


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    filterset_fields = ["category",]

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