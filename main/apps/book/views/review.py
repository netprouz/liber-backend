from rest_framework import generics
from rest_framework.response import Response
from ...common.permissions import DeletePersonalObjectPermission
from ...common.pagination import ReviewLimitOffsetPagionation
from ..models.review import Review
from ..serializers.review import ReviewCreateSerializer, ReviewListSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    model = Review
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_review_instance(
            self.request.user,
            serializer.validated_data,
        )


review_create_api_view = ReviewCreateAPIView.as_view()


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = ReviewLimitOffsetPagionation
    lookup_field = "guid"

    def get(self, request, guid):
        reviews = Review.objects.filter(book__guid=guid)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

review_list_api_view = ReviewListAPIView.as_view()


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


review_delete_api_view = ReviewDeleteAPIView.as_view()
