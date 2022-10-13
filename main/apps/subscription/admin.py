from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "guid",
        "category",
        "begin_date",
        "end_date",
        "price",
        "status",
    )
    list_display_links = ("guid",)
    list_filter = ("category", "begin_date", "end_date")
    search_fields = [
        "category__tile",
    ]
    list_editable = ("category", "begin_date", "end_date", "price")


admin.site.register(Subscription, SubscriptionAdmin)
