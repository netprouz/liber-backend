from django.urls import include, path

app_name = "book"

urlpatterns = [
    path(
        "customer/",
        include(
            ("main.apps.order.urls.customer", "main.apps.order.urls.customer"),
            namespace="",
        ),
    ),
]
