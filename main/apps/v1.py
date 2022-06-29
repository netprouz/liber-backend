from django.urls import include, path

urlpatterns = [
    path(
        "account/",
        include(
            ("main.apps.account.user", "main.apps.account.user"),
            namespace="account",
        ),
    ),
    path(
        "category/",
        include(
            ("main.apps.category.urls", "main.apps.category"),
            namespace="category",
        ),
    ),
    path(
        "book/",
        include(
            ("main.apps.book.book", "main.apps.book.book"),
            namespace="book",
        ),
    ),
    path(
        "subscription/",
        include(
            ("main.apps.subscription.urls", "main.apps.subscription.urls"),
            namespace="subscription",
        ),
    ),
    path(
        "order/",
        include(
            ("main.apps.order.order", "main.apps.order.order"),
            namespace="order",
        ),
    ),
    path(
        "statistics/",
        include(
            ("main.apps.stats.urls", "main.apps.stats.urls"),
            namespace="statistics",
        ),
    ),
    path(
        "transaction/",
        include(
            ("main.apps.transaction.urls", "main.apps.transaction.urls"),
            namespace="transaction",
        ),
    ),
]
