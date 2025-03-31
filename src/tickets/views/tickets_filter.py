from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.application.tickets_filter import FilterTickets
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class TicketsFilter(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8')) if request.body else {}

        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), 'tickets')

        app = FilterTickets(
            account_id=kwargs['account_id'],
            filters=data,
            sort=request.GET.get('sort', None),
            order=request.GET.get('order', None),
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
