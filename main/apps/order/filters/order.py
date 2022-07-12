from django_filters.rest_framework import CharFilter

from ...common.filters.base_filter import BaseFilter
from ..models import Order


class OrderFilterSet(BaseFilter):
    book_type = CharFilter(
        field_name="book_type__book_type",
        lookup_expr="exact",
    )

    class Meta:
        model = Order
        fields = ["is_paid", "is_completed", "order_number"]
