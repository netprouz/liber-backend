from django.urls import path

from . import views

urlpatterns = [
    path(
        "initialize_payment/<int:pk>/",
        view=views.initialize_payment_api_view,
        name="initialize_payment",
    ),
    path(
        "integration_with_payme/",
        view=views.accept_payme_request_view,
        name="accept_payme_requests",
    ),
    path(
        "integration_with_click/",
        view=views.accept_click_request_view,
        name="accept_click_requests",
    ),
    path(
        "list/",
        view=views.transaction_list_api_view,
        name="transaction_list",
    ),
]
