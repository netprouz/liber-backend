from django.urls import path

from ..views import review

urlpatterns = [
    path(
        "create/",
        view=review.review_create_api_view,
        name="book_review_create",
    ),
    path(
        "<uuid:guid>/delete/",
        review.review_delete_api_view,
        name="book_review_delete",
    ),
    path(
        "<uuid:guid>/list/",
        review.review_list_api_view,
        name="book_review_list",
    ),
]
