from django.db.models import Avg, Count, DecimalField, OuterRef, Subquery
from django.db.models.functions import Coalesce

from ...common.managers import BaseManager
from ..models.rate import Rate


class BookManager(BaseManager):
    def create_book_instance(self, owner, data):
        book_types = data.pop("book_types")
        instance = self.create(**data, owner=owner)
        instance.types.create_book_type(book_types)
        return instance

    def update_book_instance(self, data):
        book_types = data.pop("book_types")
        instance = self.update(**data)
        instance.types.create_book_type(book_types)
        return instance

    def filter_with_rates(self):

        output = DecimalField(max_digits=20, decimal_places=2)

        target_query = Rate.objects.filter(
            book=OuterRef("pk"),
        )
        target_query = target_query.order_by()
        target_query = target_query.annotate(
            total=Coalesce(
                Avg("point"),
                float(0),
            )
        )
        target_query = target_query.values("total")
        target_query.query.group_by = []

        books = self.annotate(
            rating=Subquery(
                target_query[:1],
                output_field=output,
            )
        )

        return books

    def filter_with_children(self):

        return self.annotate(
            view=Coalesce(
                Count("views"),
                int(0),
            ),
        ).prefetch_related("reviews",)
