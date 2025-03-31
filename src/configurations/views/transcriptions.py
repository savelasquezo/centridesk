from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken

from src.configurations.application.transcriptions import Transcriptions
from src.configurations.domain.transcription import Transcription
from src.configurations.infrastructure.transcriptions_mysql import TranscriptionsMysql


class TranscriptionsView(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        app = Transcriptions(
            account_id=kwargs['account_id'],
            info=Transcription(**data['info']),
            transcriptions_obj=TranscriptionsMysql()
        )

        return app.create()

    @api_handler
    def get(self, request, **kwargs):
        app = Transcriptions(
            account_id=kwargs['account_id'],
            transcriptions_obj=TranscriptionsMysql()
        )

        return app.get()

    @api_handler
    def put(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        app = Transcriptions(
            account_id=kwargs['account_id'],
            info=Transcription(**data['info']),
            transcriptions_obj=TranscriptionsMysql()
        )

        return app.update()
