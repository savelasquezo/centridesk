from shared.infrastructure.b64 import decode_obj
from src.customers.domain.customer_out import CustomerOut
from tests.shared.mock.data import MockData


class CustomersMysql:

    def __init__(self, account_id=None, customer=None, customer_id=None, phone=None, email=None,
                 centribot_external_id=None, exclude_id=False, mock=None):
        self.__mock = mock or MockData()

        self.account_id = account_id
        self.customer = customer
        self.customer_id = customer_id
        self.phone = phone
        self.email = email
        self.centribot_external_id = centribot_external_id
        self.exclude_id = exclude_id

        self.__encoded_fields = ['company', 'delegation', 'external_id']

    def __get(self, item, value):
        customer = None
        for c in self.__mock.customers.get(self.account_id, []):
            if c[item] == value:
                customer = CustomerOut(c).data
        return customer

    def __check(self, item, value):
        customer = None
        for c in self.__mock.customers.get(self.account_id, []):
            if c[item] == value:
                customer = c
        return customer or False

    def create(self):
        output = {
            'unique_id': self.customer.customer_id,
            'display_name': self.customer.name,
            'email': self.customer.email,
            'phone': self.customer.phone,
            'centribot_external_id': self.customer.centribot_external_id,
            'active': self.customer.active,
            'company': self.customer.company.encoded,
            'delegation': self.customer.delegation.encoded,
            'agent_id': self.customer.agent_id,
            'last_comment_at': None,
            'external_id': self.customer.external_id.encoded,
            'gdpr': self.customer.gdpr,
            'gdpr_updated_at': self.__mock.customer_created_at3,
            'created_at': self.__mock.customer_created_at3,
            'updated_at': None,
        }

        self.__mock.customers.get(self.account_id, []).append(output)

    def get_by_id(self):
        return self.__get('unique_id', self.customer_id)

    def get_by_phone(self):
        return self.__get('phone', self.phone)

    def get_by_email(self):
        return self.__get('email', self.email)

    def get_by_centribot_external_id(self):
        self.__get('centribot_external_id', self.centribot_external_id)

    def get_all(self, limit=None, offset=None):
        customers = [CustomerOut(c).data for c in self.__mock.customers.get(self.account_id, [])]
        if limit and offset:
            customers = customers[offset:offset + limit]
        return customers

    def count(self, filter_by=None, logic_operator='and'):
        customers = self.__mock.customers.get(self.account_id, [])
        if filter_by:
            customers = []
            for customer in self.__mock.customers.get(self.account_id, []):
                condition = logic_operator == 'and'
                for item, value in filter_by.items():
                    if logic_operator == 'and':
                        if isinstance(value, int):
                            if str(value) not in str(customer[item]):
                                condition = False
                                break
                        else:
                            if (not value or not customer[item]) or value not in (
                                    customer[item] if item not in self.__encoded_fields else decode_obj(
                                        customer[item])):
                                condition = False
                                break

                    if logic_operator == 'or':
                        if isinstance(value, int):
                            if str(value) in str(customer[item]):
                                condition = True
                        else:
                            if value and customer[item] and value in (
                                    customer[item] if item not in self.__encoded_fields else decode_obj(
                                        customer[item])):
                                condition = True

                if condition:
                    customers.append(customer)
        return len(customers)

    def check_by_email(self):
        return self.__check('email', self.customer.email)

    def check_by_phone(self):
        return self.__check('phone', self.customer.phone)

    def check_by_centribot_external_id(self):
        return self.__check('centribot_external_id', self.customer.centribot_external_id)

    def update(self):
        customers = self.__mock.customers.get(self.account_id, [])
        for customer in customers:
            if customer['unique_id'] == self.customer.customer_id:
                customer['display_name'] = self.customer.name
                customer['email'] = self.customer.email
                customer['phone'] = self.customer.phone
                customer['centribot_external_id'] = self.customer.centribot_external_id
                customer['active'] = self.customer.active
                customer['company'] = self.customer.company.encoded
                customer['delegation'] = self.customer.delegation.encoded
                customer['agent_id'] = self.customer.agent_id
                customer['last_comment_at'] = self.customer.last_comment_at
                customer['external_id'] = self.customer.external_id.encoded
                customer['created_at'] = self.__mock.customer_created_at3
                customer['updated_at'] = self.__mock.customer_updated_at3

                if self.customer.gdpr_updated:
                    customer['gdpr'] = int(self.customer.gdpr)
                    customer['gdpr_updated_at'] = self.__mock.customer_updated_at3

    def patch(self):
        customers = self.__mock.customers.get(self.account_id, [])
        for customer in customers:
            if customer['unique_id'] == self.customer.customer_id:
                params = {
                    'display_name': self.customer.name,
                    'email': self.customer.email,
                    'phone': self.customer.phone,
                    'updated_at': self.__mock.customer_updated_at3,
                    'company': self.customer.company.encoded,
                    'agent_id': self.customer.agent_id,
                    'delegation': self.customer.delegation.encoded
                }

                if self.customer.gdpr_updated:
                    params['gdpr'] = int(self.customer.gdpr)
                    params['gdpr_updated_at'] = self.__mock.customer_updated_at3

                for k, v in params.items():
                    if v:
                        customer[k] = v

    def update_last_comment_at(self, unique_id, timestamp):
        pass

    def delete(self):
        pass

    def filter(self, filter_by, sort=None, order=None, limit=100, offset=None, logic_operator='and'):
        sort = sort[0] if sort else None
        order = order[0] if order else None
        filtered = []
        for customer in self.__mock.customers.get(self.account_id, []):
            condition = logic_operator == 'and'
            for item, value in filter_by.items():
                if logic_operator == 'and':
                    if isinstance(value, int):
                        if str(value) not in str(customer[item]):
                            condition = False
                            break
                    else:
                        if (not value or not customer[item]) or value not in (
                                customer[item] if item not in self.__encoded_fields else decode_obj(customer[item])):
                            condition = False
                            break

                if logic_operator == 'or':
                    if isinstance(value, int):
                        if str(value) in str(customer[item]):
                            condition = True
                    else:
                        if value and customer[item] and value in (
                                customer[item] if item not in self.__encoded_fields else decode_obj(customer[item])):
                            condition = True

            if condition:
                filtered.append(customer)

        if offset:
            filtered = filtered[offset:offset + limit]
        else:
            filtered = filtered[:limit]
        if sort:
            filtered.sort(reverse=True if order == 'desc' else False, key=lambda c: c[sort])
        return [CustomerOut(c).data for c in filtered]
