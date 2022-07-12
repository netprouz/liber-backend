from django.urls import path

from . import views

urlpatterns = [
    path("on_book_type/", view=views.book_type_statistics_api_view,
         name="book_type_statistics", ),

    path("on_category/", view=views.category_statistics_api_view,
         name="category_statistics", ),

    path("on_order/", view=views.order_statistics_api_view,
         name="order_statistics", ),
    path("on_user/", view=views.user_statistics_api_view,
         name="user_statistics", ),
]
