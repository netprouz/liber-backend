from django_filters.rest_framework import DateFilter, FilterSet


class BaseFilter(FilterSet):
    begin_date = DateFilter(field_name="created_at", lookup_expr="date__gte")
    end_date = DateFilter(field_name="created_at", lookup_expr="date__lte")
