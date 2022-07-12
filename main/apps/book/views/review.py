from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..models.review import Review
from ..serializers.review import ReviewCreateSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    model = Review
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_review_instance(
            self.request.user,
            serializer.validated_data,
        )


review_create_api_view = ReviewCreateAPIView.as_view()


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


review_delete_api_view = ReviewDeleteAPIView.as_view()
