from django.urls import path

from ..views import rate

urlpatterns = [
    path(
        "create/",
        view=rate.rate_create_api_view,
        name="book_rating_create",
    ),
]
