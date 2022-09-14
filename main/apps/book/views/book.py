from importlib.resources import Resource
from unicodedata import category
from django.shortcuts import get_object_or_404
from rest_framework import generics

from main.apps.book.models.book_type import BookType, TYPEChoices
from ..models.content import Content
from main.apps.book.serializers.book_type import BookTypeSerializer
from ..serializers.content import ContentListForBookTypeSerializer
from rest_framework_simplejwt import authentication
from rest_framework import permissions

from ...common.permissions import CreatePermission  # noqa
from ...common.permissions import UpdateDeletePermission  # noqa
from ..models.book import AUDIO, ONLINE, Book
from ..serializers.book import (
    BookCreateSerializer,
    BookDetailSerializer,
    BookListSerializer,
    BookPublishedDateSerializer,
    BookUpdateSerializer
)
from ..utils import count_book_view
from ...order.models import Order
from django.db.models import Sum
from main.apps.order.serializers import OrderListSerializer
from ...book.filters.filterprice import BookFilter


class BookCreateAPIView(generics.CreateAPIView):
    model = Book
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CreatePermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


book_create_api_view = BookCreateAPIView.as_view()


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.filter_with_rates()
    serializer_class = BookListSerializer
    filterset_fields = ["title", "author", "category__id"]
    search_fields = ["title", "author", "category__title"]


book_list_api_view = BookListAPIView.as_view()


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.filter_with_children()
    serializer_class = BookDetailSerializer
    lookup_field = "guid"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            self.__class__.__name__,
            lookup_url_kwarg,
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        # count book views
        count_book_view(book=obj, user=self.request.user)
        return obj


book_detail_api_view = BookDetailAPIView.as_view()


class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


book_update_api_view = BookUpdateAPIView.as_view()


class BookDeleteAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"


book_delete_api_view = BookDeleteAPIView.as_view()


class NewAddedBookAPIView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookListSerializer
    lookup_field = 'guid'

new_added_book_api_view = NewAddedBookAPIView.as_view()


class BestSellerBookAPIView(generics.ListAPIView):
    queryset = Order.objects.annotate(quantity_sum=Sum('quantity')).order_by('-quantity_sum')[:3]
    serializer_class = OrderListSerializer

best_seller_books_api_view = BestSellerBookAPIView.as_view()
 

class AudioBooksAPIView(generics.ListAPIView):
    queryset = Content.objects.filter(book_type=AUDIO)
    serializer_class = ContentListForBookTypeSerializer

audio_book_api_view = AudioBooksAPIView.as_view()


class OnlineBookAPIView(generics.ListAPIView):
    queryset = Content.objects.filter(book_type=ONLINE)
    serializer_class = ContentListForBookTypeSerializer

online_book_api_view = OnlineBookAPIView.as_view()


class BookPulishedDateFilterAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    search_fields = ["published_date", "category__id"]


book_publisheddate_filter_api_view = BookPulishedDateFilterAPIView.as_view()

from rest_framework.response import Response

class BookFilterAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_class = BookFilter
    search_fields = ["title", "published_date",]

    def get_queryset(self):
        new_books = self.request.query_params.get('new')
        old_books = self.request.query_params.get('old')

        if new_books:
            qs = Book.objects.all().order_by('-created_at')
        elif old_books:
            qs = Book.objects.all().order_by('created_at')
            return qs
        return super().get_queryset()

book_filter_api_view = BookFilterAPIView.as_view()


class BookPublishedDateView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookPublishedDateSerializer


book_published_date_list = BookPublishedDateView.as_view()


class OldBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_class = BookFilter
    search_fields = ["title", "published_date",]


old_books_api_view = OldBooksAPIView.as_view()



# class BookPriceAPIView(generics.ListAPIView):
#     data = BookType.objects.all()
#     product_ser = BookTypeSerializer(data, many=True)

#     min_price = min(product_ser.data, key=lambda x: x["price"])
#     max_price = max(product_ser.data, key=lambda x: x["price"])

# book_price_api_view = BookPriceAPIView.as_view()