from django.urls import path

from ..views import favourite

urlpatterns = [
    path(
        "list/",
        view=favourite.favourite_list_api_view,
        name="favourite_book_list",
    ),
    path(
        "create/",
        view=favourite.favourite_create_api_view,
        name="favourite_book_create",
    ),
    path(
        "<uuid:guid>/delete/",
        favourite.favourite_delete_api_view,
        name="favourite_book_delete",
    ),
]
