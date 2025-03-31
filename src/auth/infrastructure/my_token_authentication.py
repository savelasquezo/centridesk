from rest_framework.authentication import TokenAuthentication

from api.models.token.my_token import MyToken


class MyTokenAuthentication(TokenAuthentication):
    model = MyToken
