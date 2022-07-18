from ..models.book_type import BookType
from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter


class BookPriceRangeFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = BookType
        fields = (
            'min_price',
            'max_price'
            )