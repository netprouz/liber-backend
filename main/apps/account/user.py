from django.urls import include, path

app_name = "account"

urlpatterns = [
    path(
        "",
        include(
            ("main.apps.account.urls.user", "main.apps.account.urls.user"),
            namespace="",
        ),
    ),
    path(
        "balance/",
        include(
            (
                "main.apps.account.urls.balance",
                "main.apps.account.urls.balance",
            ),
            namespace="balance",
        ),
    ),
    path(
        "online_book/",
        include(
            (
                "main.apps.account.urls.online_book",
                "main.apps.account.urls.online_book",
            ),
            namespace="online_book",
        ),
    ),
    path(
        "audio_book/",
        include(
            (
                "main.apps.account.urls.audio_book",
                "main.apps.account.urls.audio_book",
            ),
            namespace="audio_book",
        ),
    ),
]
