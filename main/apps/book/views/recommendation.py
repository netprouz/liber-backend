from rest_framework import generics

from ...common.permissions import CreatePermission
from ..filters.recommendation import RecommendationFilterSet
from ..models.recommendation import Recommendation
from ..serializers.recommendation import (
    RecommendationCreateSerializer,
    RecommendationListSerializer,
)


class RecommendationCreateAPIView(generics.CreateAPIView):
    model = Recommendation
    serializer_class = RecommendationCreateSerializer
    permission_classes = [CreatePermission]

    def perform_create(self, serializer):
        return self.model.objects.create_recommendation_instance(
            self.request.user,
            serializer.validated_data,
        )


recommendation_create_api_view = RecommendationCreateAPIView.as_view()


class RecommendationListAPIView(generics.ListAPIView):
    queryset = Recommendation.objects.filter_recommendation()
    serializer_class = RecommendationListSerializer
    filterset_class = RecommendationFilterSet
    search_fields = ["book__title", "book__author"]


recommendation_list_api_view = RecommendationListAPIView.as_view()


class RecommendationDeleteAPIView(generics.DestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationCreateSerializer
    lookup_field = "guid"


recommendation_delete_api_view = RecommendationDeleteAPIView.as_view()
