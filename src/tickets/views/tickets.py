from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.firebase.infrastructure.firebase_connector import FirebaseConnector
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.auth.infrastructure.users_token_orm import UsersTokenOrm
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.comments.infrastructure.comments_mysql import CommentsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.application.ticket_create import TicketCreate
from src.tickets.application.tickets_get import GetTickets
from src.tickets.domain.ticket_create_in import TicketIn
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql
from src.tickets.infrastructure.websocket import TicketsWebsocket


class Tickets(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        app = TicketCreate(
            account_id=kwargs['account_id'],
            ticket=TicketIn(**data),
            tickets_obj=TicketsMysql(),
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            priority_obj=PrioritiesOrm(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql(),
            agents_obj=AgentsMysql(),
            websocket_obj=TicketsWebsocket(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm()
        )

        return app.create()

    @api_handler
    def get(self, request, **kwargs):
        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), 'tickets')

        app = GetTickets(
            account_id=kwargs['account_id'],
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict={s['id']: s['name'] for s in StatusOrm().get_all()},
            priorities_dict={p['id']: p['name'] for p in PrioritiesOrm().get_all()},
            channels_dict={c['id']: c['name'] for c in ChannelsMysql().get_all()},
            page=paginator.page,
            page_size=paginator.page_size
        )

        paginator.results, paginator.total = app.get()

        return paginator.get_response()
