from django.urls import path

from ..views import audio_book

urlpatterns = [
    path(
        "list/",
        view=audio_book.audio_book_list_api_view,
        name="online_book_list",
    ),
    path(
        "<uuid:guid>/detail/",
        audio_book.audio_book_detail_api_view,
        name="online_book_detail",
    ),
    path(
        "<uuid:guid>/delete/",
        audio_book.audio_book_delete_api_view,
        name="audio_book_delete",
    ),
]
