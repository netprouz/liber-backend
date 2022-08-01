from django.urls import path

from ..views import user

urlpatterns = [
    path("login/", view=user.user_login_view, name="user_login"),
    path("logout/", view=user.user_logout_view, name="user_logout"),
    path("list/", view=user.user_list_view, name="user_list"),
    path(
        "generate/password/",
        view=user.user_generate_password_view,
        name="user_generate_password",
    ),
    path(
        "<uuid:guid>/detail/",
        user.user_detail_api_view,
        name="user_detail",
    ),
    path(
        "<uuid:guid>/update/",
        user.user_update_api_view,
        name="user_update",
    ),

    path('register/', user.user_registration_api_view, name='register'),

    path('user-login/', user.user_login_api_view, name='user-login'),

    path('verify-phone/', user.user_otp_verify_api_view, name='verify-phhone'),
]
