# from secrets import choice
from main.apps.book.serializers.book_type import BookTypeSerializer
from ..models.book_type import BookType, TYPEChoices
from ..models.book import Book
from django_filters import FilterSet
from django_filters import NumberFilter
from django_filters import filters



class BookFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    book_type = filters.CharFilter(field_name='book_type',  label="Book Type")
    # published_date = filters.CharFilter(
    #     field_name='published_date__year',  label='Published date')
    published_date = filters.CharFilter(field_name='book__published_date', label='Published Date')

    
    class Meta:
        model = BookType
        fields = (
            'min_price',
            'max_price',
            'book_type',
            'published_date'
            )


