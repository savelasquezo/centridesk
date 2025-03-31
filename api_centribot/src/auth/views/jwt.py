from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api_centribot.models.users.catuser import CATUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Class to customize the content of the JWT payload. Instead of using the autoincremental ID
    for the user, use the UUID instead
    """

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['user_id'] = CATUser.objects.get(user_id=token['user_id']).unique_id

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
