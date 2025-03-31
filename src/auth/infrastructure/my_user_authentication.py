from django.contrib.auth.models import User, update_last_login

from shared.exceptions.unauthorized import Unauthorized


class MyUserAuthentication:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def check_user_password(self):
        try:
            auth_user = User.objects.get(username=self.username)

        except Exception as ex:
            raise Unauthorized(ex)

        else:
            if auth_user.check_password(self.password):
                update_last_login(None, auth_user)
                return auth_user

        raise Unauthorized()
