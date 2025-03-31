from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.customers.application.delete_customer import DeleteCustomer
from src.customers.application.edit_customer import EditCustomer
from src.customers.application.get_customer import GetCustomer
from src.customers.domain.customer_in import CustomerIn
from src.customers.infrastructure.customers_mysql import CustomersMysql


class Customer(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetCustomer(
            customer_id=kwargs['customer_id'],
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql()
        )

        return app.get()

    @api_handler
    def put(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        customer = CustomerIn(
            customer_id=kwargs['customer_id'],
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            centribot_external_id=data.get('centribot_external_id'),
            agent_id=data.get('agent_id'),
            company=data.get('company'),
            delegation=data.get('delegation'),
            active=data.get('active'),
            external_id=data.get('external_id'),
            gdpr=data.get('gdpr')
        )

        app = EditCustomer(
            customer=customer,
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql()
        )

        return app.edit()

    @api_handler
    def patch(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        customer = CustomerIn(
            customer_id=kwargs['customer_id'],
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            company=data.get('company'),
            delegation=data.get('delegation'),
            external_id=data.get('external_id'),
            gdpr=data.get('gdpr'),
            patch=True
        )

        app = EditCustomer(
            customer=customer,
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            patch=True
        )

        return app.edit()

    @staticmethod
    def delete(request, **kwargs):
        app = DeleteCustomer(
            customer_id=kwargs['customer_id'],
            account_id=kwargs['account_id'],
            customers_obj=CustomersMysql()
        )
        app.delete()

        return Response({'message': 'ok'}, 200)
