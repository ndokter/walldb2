from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailAuthenticationBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return

        if user and user.check_password(password):
            return user

        return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
        