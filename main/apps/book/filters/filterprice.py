from random import choices
from ..models.book_type import BookType, TYPEChoices
from ..models.book import Book
from django_filters import FilterSet
from django_filters import NumberFilter
import django_filters
from django_filters import filters


class BookPriceRangeFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = BookType
        fields = (
            'min_price',
            'max_price'
            )

class BookFilter(FilterSet):
    category = filters.CharFilter(field_name='category__id', lookup_expr='iexact', label='Category')
    published_date = django_filters.DateFilter(field_name='published_date', input_formats=[
        "%Y", "%Y"], lookup_expr='gte', label='Published date')
    min_price = NumberFilter(field_name='types__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='types__price', lookup_expr='lte')
    # book_type = filters.ChoiceFilter(field_name='book_type', choices=TYPEChoices)

    class Meta:
        model = Book
        fields = (
            'min_price',
            'max_price',
            'category',
            # 'book_type',
            'published_date'
            )


