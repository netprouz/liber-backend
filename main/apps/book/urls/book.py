from django.urls import path

from ..views import book

urlpatterns = [
    path("list/", view=book.book_list_api_view, name="book_list"),
    path(
        "create/",
        view=book.book_create_api_view,
        name="book_create",
    ),
    path(
        "<uuid:guid>/detail/",
        book.book_detail_api_view,
        name="book_detail",
    ),
    path(
        "<uuid:guid>/update/",
        book.book_update_api_view,
        name="book_update",
    ),
    path(
        "<uuid:guid>/delete/",
        book.book_delete_api_view,
        name="book_delete",
    ),
]
