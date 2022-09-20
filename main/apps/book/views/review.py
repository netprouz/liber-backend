from rest_framework import generics
from rest_framework.response import Response
from ...common.permissions import DeletePersonalObjectPermission
from ..models.review import Review
from ..serializers.review import ReviewCreateSerializer, ReviewListSerializer
from ...common.pagination import ReviewLimitOffsetPagionation


class ReviewCreateAPIView(generics.CreateAPIView):
    model = Review
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_review_instance(
            self.request.user,
            serializer.validated_data,
        )


review_create_api_view = ReviewCreateAPIView.as_view()


# class ReviewListAPIView(APIView):
#     # queryset = Review.objects.filter_review()
#     # serializer_class = ReviewListSerializer
#     # lookup_field = "guid"
#     # paginate_by = 1
#     # def get_queryset(self):
#     #     return self.queryset.filter(owner=self.request.user)
#     def get(request, guid):
#         reviews = Review.objects.filter(book__guid=guid)
#         serializer = ReviewListSerializer(reviews, many=True)
#         return Response(serializer.data)

class ReviewListAPIView(generics.ListAPIView):
    pagination_class = ReviewLimitOffsetPagionation
    def get_queryset(self):
        queryset = Review.objects.filter(book__guid=self.kwargs['guid'])
        return queryset
    serializer_class = ReviewListSerializer

review_list_api_view = ReviewListAPIView.as_view()


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


review_delete_api_view = ReviewDeleteAPIView.as_view()
