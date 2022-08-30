# from secrets import choice
from main.apps.book.serializers.book_type import BookTypeSerializer
from ..models.book_type import BookType, TYPEChoices
from ..models.book import Book
from django_filters import FilterSet
from django_filters import NumberFilter
from django_filters import filters



class BookFilter(FilterSet):
    category = filters.CharFilter(field_name='category__title', lookup_expr='iexact', label='Category')
    min_price = NumberFilter(field_name='types__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='types__price', lookup_expr='lte')
    book_type = filters.CharFilter(field_name='types__book_type',  label="Book Type")
    
    class Meta:
        model = Book
        fields = (
            'min_price',
            'max_price',
            'category',
            'book_type',
            )


