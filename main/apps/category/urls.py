from django.urls import path

from . import views

app_name = "category"

urlpatterns = [
    path("list/", view=views.category_list_api_view, name="category_list"),
    path(
        "create/",
        view=views.category_create_api_view,
        name="category_create",
    ),
    path(
        "<uuid:guid>/update/",
        views.category_update_api_view,
        name="category_update",
    ),
    path(
        "<uuid:guid>/delete/",
        views.category_delete_api_view,
        name="category_delete",
    ),
]
