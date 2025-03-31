from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from api_centribot.models.users.catuser import CATUser


class MyJWTAuthentication(JWTAuthentication):
    @classmethod
    def get_user(cls, validated_token):
        """
            Attempts to find and return a user using the given validated token. This overwrite
            is required in order to use the UUID for user_id.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            user_id = CATUser.objects.get(unique_id=user_id).user_id
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})

        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive', code='user_inactive')

        return user
