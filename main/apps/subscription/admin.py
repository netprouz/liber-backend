from django.contrib import admin

from .models import Subscription,SubscriptionTransaction


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


class SubscriptionTransactionModelAdmin(admin.ModelAdmin):

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'status'

    search_fields = ('request_id',)
    list_display = ['trans_id', 'request_id', 'amount', 'account', 'get_status', 'create_time', 'pay_time']


admin.site.register(SubscriptionTransaction, SubscriptionTransactionModelAdmin)