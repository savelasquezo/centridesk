from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.firebase.infrastructure.firebase_connector import FirebaseConnector
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.auth.infrastructure.users_token_orm import UsersTokenOrm
from src.centribot.infrasctructure.centribot_requests import CentribotRequests
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.application.ticket_edit import EditTicket
from src.tickets.application.ticket_get import GetTicket
from src.tickets.domain.ticket_edit_in import TicketEditIn
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql
from src.tickets.infrastructure.websocket import TicketsWebsocket


class Ticket(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetTicket(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict={s['id']: s['name'] for s in StatusOrm().get_all()},
            priorities_dict={p['id']: p['name'] for p in PrioritiesOrm().get_all()},
            channels_dict={c['id']: c['name'] for c in ChannelsMysql().get_all()}
        )
        return app.get()

    @api_handler
    def put(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        status_dict = {s['id']: s['name'] for s in StatusOrm().get_all()}
        priorities_dict = {p['id']: p['name'] for p in PrioritiesOrm().get_all()}
        channels_dict = {c['id']: c['name'] for c in ChannelsMysql().get_all()}

        tickets_obj = TicketsMysql()
        customers_obj = CustomersMysql()
        agents_obj = AgentsMysql()

        getter = GetTicket(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            tickets_obj=tickets_obj,
            customers_obj=customers_obj,
            agents_obj=agents_obj,
            status_dict=status_dict,
            priorities_dict=priorities_dict,
            channels_dict=channels_dict
        )
        ticket_bkup = getter.get()

        app = EditTicket(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            ticket=TicketEditIn(
                ticket_id=data.get('id'),
                assignee_id=data.get('assignee_id', ticket_bkup['assignee_id']),
                status=data.get('status', ticket_bkup['status']),
                status_id=data.get('status_id', ticket_bkup['status_id']),
                priority=data.get('priority', ticket_bkup['priority']),
                priority_id=data.get('priority_id', ticket_bkup['priority_id']),
                external_id=data.get('external_id', ticket_bkup['external_id']),
                tags=data.get('tags', [])
            ),
            ticket_bkup=ticket_bkup,
            tickets_obj=tickets_obj,
            customers_obj=customers_obj,
            agents_obj=agents_obj,
            centribot_obj=CentribotRequests(),
            status_dict=status_dict,
            priorities_dict=priorities_dict,
            websocket_obj=TicketsWebsocket(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm()
        )
        app.edit()

        return getter.get()
