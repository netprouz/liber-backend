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


class FavouriteListAPIView(generics.ListAPIView):
    queryset = Favourite.objects.filter_favourites()
    serializer_class = FavouriteListSerializer
    filterset_class = FavouriteFilterSet
    search_fields = ["book__title", "book__author"]


favourite_list_api_view = FavouriteListAPIView.as_view()



class FavouriteDeleteAPIView(generics.DestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteListSerializer
    permission_classes = [DeletePersonalObjectPermission]
    lookup_field = "guid"


favourite_delete_api_view = FavouriteDeleteAPIView.as_view()
