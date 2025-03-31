from time import sleep

from shared.exceptions.generic import GenericException
from shared.exceptions.in_use import InUse
from shared.exceptions.not_found import NotFound
from src.customers.application.get_customer import GetCustomer


class CreateCustomer:

    def __init__(self, customer, account_id, customers_obj, agents_obj):
        self.customer = customer
        self.account_id = account_id
        self.customers_obj = customers_obj
        self.agents_obj = agents_obj

    def create(self):
        self.customers_obj.customer = self.customer
        self.customers_obj.account_id = self.account_id

        # check email phone and external_id are not in use
        if self.customer.email and self.customers_obj.check_by_email():
            raise InUse('email')

        if self.customer.phone and self.customers_obj.check_by_phone():
            raise InUse('phone')

        if self.customer.centribot_external_id and self.customers_obj.check_by_centribot_external_id():
            raise InUse('centribot external id')

        if self.customer.agent_id:
            self.agents_obj.agent_id = self.customer.agent_id
            self.agents_obj.account_id = self.account_id
            if not self.agents_obj.get_user_account_by_user_and_account():
                raise GenericException('Agent not in account')
            user_role = self.agents_obj.get_user_rol_by_user()
            if not user_role:
                raise GenericException('Agent role not valid')
            else:
                role = self.agents_obj.get_role(user_role['role_id'])
                if not role['desk']:
                    raise GenericException('Agent role not valid')

        self.customers_obj.create()

        getter = GetCustomer(
            customer_id=self.customer.customer_id,
            account_id=self.account_id,
            customers_obj=self.customers_obj
        )

        try:
            customer = getter.get()
        except NotFound:
            sleep(1)
            customer = getter.get()

        return customer
