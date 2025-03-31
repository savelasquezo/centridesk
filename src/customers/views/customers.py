from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.customers.application.create_customer import CreateCustomer
from src.customers.application.get_customers import GetCustomers
from src.customers.domain.customer_in import CustomerIn
from src.customers.infrastructure.customers_mysql import CustomersMysql


class Customers(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), 'customers')

        app = GetCustomers(
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql(),
            page=paginator.page,
            page_size=paginator.page_size
        )

        paginator.results, paginator.total = app.get()

        return paginator.get_response()

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        customer = CustomerIn(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            centribot_external_id=data.get('centribot_external_id'),
            agent_id=data.get('agent_id'),
            company=data.get('company'),
            delegation=data.get('delegation'),
            external_id=data.get('external_id'),
            gdpr=data.get('gdpr', True)
        )

        app = CreateCustomer(
            customer=customer,
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql()
        )

        return app.create()
