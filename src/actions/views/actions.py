from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.async_queue.infrastructure.sender_centridesk_generics import AsyncSenderGeneric
from src.actions.application.create import CreateAction
from src.actions.domain.action_in import Action
from src.actions.infrastructure.actions_mysql import ActionsMysql


class Actions(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        action = Action(
            action=data.get('action'),
            info=data.get('info'),
            account_id=kwargs['account_id'],
            requester_id=request.user.catuser.unique_id
        )

        # initiate action process
        app = CreateAction(
            action=action,
            actions_obj=ActionsMysql(),
            async_sender_obj=AsyncSenderGeneric()
        )

        return app.create()
