from django.urls import include, path

app_name = "book"

urlpatterns = [
    path(
        "",
        include(
            ("main.apps.book.urls.book", "main.apps.book.urls.book"),
            namespace="",
        ),
    ),
    path(
        "content/",
        include(
            ("main.apps.book.urls.content", "main.apps.book.urls.content"),
            namespace="content",
        ),
    ),
    path(
        "rate/",
        include(
            ("main.apps.book.urls.rate", "main.apps.book.urls.rate"),
            namespace="rate",
        ),
    ),
    path(
        "review/",
        include(
            ("main.apps.book.urls.review", "main.apps.book.urls.review"),
            namespace="review",
        ),
    ),
    path(
        "favourite/",
        include(
            ("main.apps.book.urls.favourite", "main.apps.book.urls.favourite"),
            namespace="favourite",
        ),
    ),
    path(
        "recommendation/",
        include(
            (
                "main.apps.book.urls.recommendation",
                "main.apps.book.urls.recommendation",
            ),
            namespace="recommendation",
        ),
    ),
]
