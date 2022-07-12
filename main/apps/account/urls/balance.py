from django.urls import path

from ..views import balance

urlpatterns = [
    path(
        "create/",
        view=balance.balance_create_api_view,
        name="user_balance_create",
    ),
    path(
        "<uuid:guid>/delete/",
        balance.balance_delete_api_view,
        name="user_balance_delete",
    ),
]
