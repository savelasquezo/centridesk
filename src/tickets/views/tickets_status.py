from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.tickets.application.status_get import GetTicketsStatus
from src.tickets.infrastructure.status_orm import StatusOrm


class TicketsStatus(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetTicketsStatus(status_obj=StatusOrm())
        return app.get()
