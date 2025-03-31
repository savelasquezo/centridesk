from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.channels.application.get_channels import GetChannels
from src.channels.infrastructure.channels_mysql import ChannelsMysql


class Channels(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetChannels(
            channels_obj=ChannelsMysql()
        )
        return app.get()
