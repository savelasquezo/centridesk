from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.customers.application.search_customers import SearchCustomers
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.search.domain.query_type import QueryType
from src.search.domain.search_customer import SearchCustomer
from src.search.domain.search_ticket import SearchTicket
from src.tickets.application.tickets_search import SearchTickets
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class GenericSearch(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        query_type = QueryType(kwargs['type'])
        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), query_type.query_type)

        # All searches of generic search
        searches_dict = {
            'customers': SearchCustomer,
            'tickets': SearchTicket
        }

        # All applications of generic search
        apps_dict = {
            'customers': lambda s: SearchCustomers(
                account_id=kwargs['account_id'],
                customers_obj=CustomersMysql(),
                page=paginator.page,
                page_size=paginator.page_size,
                search=s,
                tickets_obj=TicketsMysql(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql()
            ).get(),
            'tickets': lambda s: SearchTickets(
                account_id=kwargs['account_id'],
                tickets_obj=TicketsMysql(),
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql(),
                status_dict={s['id']: s['name'] for s in StatusOrm().get_all()},
                priorities_dict={p['id']: p['name'] for p in PrioritiesOrm().get_all()},
                channels_dict={c['id']: c['name'] for c in ChannelsMysql().get_all()},
                page=paginator.page,
                page_size=paginator.page_size,
                search=s
            ).get()
        }

        # Generic Search
        search = searches_dict.get(query_type.query_type)(request.GET.get('query', None), request.GET.get('sort', None),
                                                          request.GET.get('order', None))

        paginator.results, paginator.total = apps_dict.get(query_type.query_type)(search)

        return paginator.get_response()
