from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "guid",
        "category",
        "active",
        "begin_date",
        "end_date",
        "price",
        "active",
    )
    list_display_links = ("guid",)
    list_filter = ("category", "begin_date", "end_date", "active")
    search_fields = [
        "category__tile",
    ]
    list_editable = ("category", "begin_date", "end_date", "price", "active")


admin.site.register(Subscription, SubscriptionAdmin)
