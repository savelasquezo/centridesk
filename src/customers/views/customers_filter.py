from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.customers.application.filter_customers import FilterCustomers
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class CustomersFilter(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))
        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), 'customers')

        app = FilterCustomers(
            account_id=kwargs['account_id'],
            filters=data,
            sort=request.GET.get('sort', None),
            order=request.GET.get('order', None),
            customers_obj=CustomersMysql(),
            page=paginator.page,
            page_size=paginator.page_size,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )

        paginator.results, paginator.total = app.get()

        return paginator.get_response()
