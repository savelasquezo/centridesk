from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.tickets.application.priorities_get import GetTicketPriorities
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm


class TicketPriorities(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetTicketPriorities(priorities_obj=PrioritiesOrm())
        return app.get()
