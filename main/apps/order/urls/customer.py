from django.urls import path
from ..views import customer


urlpatterns = [
    path("list/", view=customer.order_list_api_view, name="order_list"),
    path("all-orders/", view=customer.all_order_api_view, name="order_list"),
    path(
        "create/",
        view=customer.order_create_api_view,
        name="order_create",
    ),
    path(
        "<uuid:guid>/complete/",
        view=customer.oder_complete_api_view,
        name="order_complete",
    ),
]
