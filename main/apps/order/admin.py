from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "guid",
        "book",
        "book_type",
        "order_number",
        "total_price",
        "owner",
        "is_paid",
        "is_completed",
    )
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "book_type",
        "order_number",
        "owner",
        "is_paid",
        "is_completed",
    )
    search_fields = [
        "book__tile",
        "order_number",
    ]
    list_editable = ("book", "book_type", "owner", "is_paid", "is_completed")


admin.site.register(Order, OrderAdmin)
