from django.urls import path

from . import views

urlpatterns = [
    path(
        "list/",
        view=views.subscription_list_api_view,
        name="subscription_list",
    ),
    path(
        "list/get/",
        view=views.subscription_view,
        name="subscription_list",
    ),
    path(
        "create/",
        view=views.subscription_create_api_view,
        name="subscription_create",
    ),
]
