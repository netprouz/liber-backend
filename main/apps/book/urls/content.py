from django.urls import path

from ..views import content

urlpatterns = [
    path(
        "list/",
        view=content.content_list_api_view,
        name="book_content_list",
    ),
    path(
        "create/",
        view=content.content_create_api_view,
        name="book_content_create",
    ),
    path(
        "<uuid:guid>/detail/",
        content.content_detail_api_view,
        name="book_content_detail",
    ),
    path(
        "<uuid:guid>/update/",
        content.content_update_api_view,
        name="book_content_update",
    ),
    path(
        "<uuid:guid>/delete/",
        content.content_delete_api_view,
        name="book_content_delete",
    ),
]
