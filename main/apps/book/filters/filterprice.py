from ..models.book_type import BookType, TYPEChoices
from ..models.book import Book
from django_filters import FilterSet
from django_filters import NumberFilter
from django_filters import filters


class BookFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = NumberFilter(field_name='price', lookup_expr='lte', label="Max Price")
    category = filters.CharFilter(field_name='book__category__title', lookup_expr='iexact', label='Category') 
    book_type = filters.ModelChoiceFilter(field_name='book_type',label="Book type", choices=TYPEChoices, queryset=BookType.objects.all())

    class Meta:
        model = BookType
        fields = (
            'min_price',
            'max_price',
            'category', 
            'book_type'
            )

# class BookFilter(FilterSet):
#     category = filters.CharFilter(field_name='category__id', lookup_expr='iexact', label='Category')
#     published_date = filters.DateFilter(field_name='published_date', input_formats=[
#         "%Y", "%Y"], lookup_expr='iexact', label='Published date')
#     min_price = NumberFilter(field_name='types__book_type__price', lookup_expr='gte')
#     max_price = NumberFilter(field_name='types__book_type__price', lookup_expr='lte')
#     # book_type = filters.ChoiceFilter(field_name='book_type', choices=TYPEChoices)

#     class Meta:
#         model = Book
#         fields = (
#             'min_price',
#             'max_price',
#             'category',
#             # 'book_type',
#             'published_date'
#             )


