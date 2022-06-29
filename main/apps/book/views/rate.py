from rest_framework import generics

from ..models.rate import Rate
from ..serializers.rate import RateCreateUpdateSerializer


class RateCreateAPIView(generics.CreateAPIView):
    model = Rate
    serializer_class = RateCreateUpdateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_rate_instance(
            self.request.user,
            serializer.validated_data,
        )


rate_create_api_view = RateCreateAPIView.as_view()
