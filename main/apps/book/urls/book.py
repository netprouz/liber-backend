from django.urls import path

from ..views import book

urlpatterns = [
    path("list/", view=book.book_list_api_view, name="book_list"),

    path("new-books/", view=book.new_added_book_api_view, name="new_book_list"),

    path("best-seller/", view=book.best_seller_books_api_view, name="best_seller_books"),

    path("book-publisheddate/", view=book.book_publisheddate_filter_api_view, name="published_date"),

    path("online-books/", view=book.online_book_api_view, name="online_books"),

    path("audio-books/", view=book.audio_book_api_view, name="audio_books"),

    path("price-filter/", view=book.book_filter_by_range_api_view, name="price_filter"),

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
