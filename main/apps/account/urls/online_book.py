from django.urls import path

from ..views import online_book

urlpatterns = [
    path(
        "list/",
        view=online_book.online_book_list_api_view,
        name="online_book_list",
    ),
    path(
        "<uuid:guid>/detail/",
        online_book.online_book_detail_api_view,
        name="online_book_detail",
    ),
    path(
        "<uuid:guid>/delete/",
        online_book.online_book_delete_api_view,
        name="online_book_delete",
    ),
]
