from django.urls import path

from ..views import recommendation

urlpatterns = [
    path(
        "list/",
        view=recommendation.recommendation_list_api_view,
        name="recommendation_book_list",
    ),
    path(
        "create/",
        view=recommendation.recommendation_create_api_view,
        name="recommendation_book_create",
    ),
    path(
        "<uuid:guid>/delete/",
        recommendation.recommendation_delete_api_view,
        name="recommendation_book_delete",
    ),
]
