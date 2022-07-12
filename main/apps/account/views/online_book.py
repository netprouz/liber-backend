from rest_framework import generics

from ...common.permissions import DeletePersonalObjectPermission
from ..models.online_book import OnlineBook
from ..serializers import online_book


class OnlineBookListAPIView(generics.ListAPIView):
    queryset = OnlineBook.objects.filter_with_rates()
    serializer_class = online_book.OnlineBookSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


online_book_list_api_view = OnlineBookListAPIView.as_view()


class OnlineBookDetailAPIView(generics.RetrieveAPIView):
    queryset = OnlineBook.objects.all()
    serializer_class = online_book.OnlineBookDetailSerializer
    permission_classes = [DeletePersonalObjectPermission, ]
    lookup_field = "guid"


online_book_detail_api_view = OnlineBookDetailAPIView.as_view()


class OnlineBookDeleteAPIView(generics.DestroyAPIView):
    queryset = OnlineBook.objects.all()
    serializer_class = online_book.OnlineBookDetailSerializer
    permission_classes = [DeletePersonalObjectPermission, ]
    lookup_field = "guid"


online_book_delete_api_view = OnlineBookDeleteAPIView.as_view()
