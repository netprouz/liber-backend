from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..filters.favourite import FavouriteFilterSet
from ..models.favourite import Favourite
from ..serializers.favourite import (
    FavouriteCreateSerializer,
    FavouriteListSerializer,
)


class FavouriteCreateAPIView(generics.CreateAPIView):
    model = Favourite
    serializer_class = FavouriteCreateSerializer

    def perform_create(self, serializer):
        return self.model.objects.create_favourite_instance(
            self.request.user,
            serializer.validated_data,
        )


favourite_create_api_view = FavouriteCreateAPIView.as_view()


from ...book.models.review import Review
from django.db.models import Avg
from rest_framework.response import Response

class FavouriteListAPIView(generics.ListAPIView):
    queryset = Favourite.objects.filter_favourites()
    serializer_class = FavouriteListSerializer
    filterset_class = FavouriteFilterSet
    search_fields = ["book__title", "book__author"]


    # def get(self, request):
    #     fav = Favourite.objects.filter_favourites()
    #     review_count = Review.objects.filter(book__guid=self.kwargs['guid'])
    #     rate_avg = Review.objects.filter(book__guid=self.kwargs['guid']).aggregate(Avg('point'))
    #     data = {
    #         'review_count': review_count,
    #         'rate_avg': rate_avg,
    #         'fav': fav
    #     }
    #     return Response(data)

favourite_list_api_view = FavouriteListAPIView.as_view()


class FavouriteDeleteAPIView(generics.DestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteListSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


favourite_delete_api_view = FavouriteDeleteAPIView.as_view()
