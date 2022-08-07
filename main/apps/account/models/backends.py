from . import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


class EmailPhoneUsernameAuthenticationBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None


    def authenticate(self, username, password):
        try:
            user = User.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None