from shared.mysql.infrastructure.mysql_methods import MysqlMethods
from src.customers.domain.customer_out import CustomerOut


class CustomersMysql:

    def __init__(self, account_id=None, customer=None, customer_id=None, phone=None, email=None,
                 centribot_external_id=None, exclude_id=False):
        self.__table = 'customers'
        self.__db = MysqlMethods('centridesk')

        self.__opts = ['id', 'unique_id', 'agent_id', 'display_name', 'email', 'phone', 'centribot_external_id',
                       'company', 'delegation', 'last_comment_at', 'created_at', 'updated_at', 'active', 'external_id',
                       'gdpr', 'gdpr_updated_at']

        self.__encoded_fields = ['company', 'delegation', 'external_id']

        self.account_id = account_id
        self.customer = customer
        self.customer_id = customer_id
        self.phone = phone
        self.email = email
        self.centribot_external_id = centribot_external_id
        self.exclude_id = exclude_id

    def __get(self, item, value):
        condition = {item: {'op': '=', 'value': value}}
        user = self.__db.select_one(self.account_id, self.__table, self.__opts, conditions=condition)
        return CustomerOut(user).data

    def __check(self, item, value):
        condition = {item: {'op': '=', 'value': value}}

        if self.exclude_id:
            condition['unique_id'] = {'op': '!=', 'value': self.customer.customer_id}

        user = self.__db.select_one(self.account_id, self.__table, self.__opts, conditions=condition)
        return user or False

    def create(self):
        params = {
            'unique_id': self.customer.customer_id,
            'display_name': self.customer.name,
            'email': self.customer.email,
            'phone': self.customer.phone,
            'centribot_external_id': self.customer.centribot_external_id,
            'created_at': self.customer.timestamp_at,
            'active': self.customer.active,
            'company': self.customer.company.encoded,
            'agent_id': self.customer.agent_id,
            'delegation': self.customer.delegation.encoded,
            'external_id': self.customer.external_id.encoded,
            'gdpr': self.customer.gdpr,
            'gdpr_updated_at': self.customer.timestamp_at
        }
        self.__db.insert(self.account_id, self.__table, params)

    def get_by_id(self):
        return self.__get('unique_id', self.customer_id)

    def get_by_phone(self):
        return self.__get('phone', self.phone)

    def get_by_email(self):
        return self.__get('email', self.email)

    def get_by_centribot_external_id(self):
        self.__get('centribot_external_id', self.centribot_external_id)

    def get_all(self, limit=None, page=None):
        customers = self.__db.select(self.account_id, self.__table, self.__opts, limit=limit, page=page)
        return [CustomerOut(c).data for c in customers]

    def count(self, filter_by=None, logic_operator='and'):
        conditions = {}
        if filter_by:
            for item, value in filter_by.items():
                if item in self.__encoded_fields:
                    conditions[
                        f'lower(json_unquote(json_extract(convert(from_base64({item}) using utf8mb4), "$[0]")))'] = {
                        'op': 'like', 'value': f"%{value.lower()}%"}
                else:
                    conditions[item] = {'op': 'like', 'value': f"%{value}%"}
        return self.__db.select(self.account_id, self.__table, ['count(id)'], conditions=conditions,
                                logic_operator=logic_operator)[0].get('count(id)')

    def check_by_email(self):
        return self.__check('email', self.customer.email)

    def check_by_phone(self):
        return self.__check('phone', self.customer.phone)

    def check_by_centribot_external_id(self):
        return self.__check('centribot_external_id', self.customer.centribot_external_id)

    def update(self):
        params = {
            'display_name': self.customer.name,
            'email': self.customer.email,
            'phone': self.customer.phone,
            'centribot_external_id': self.customer.centribot_external_id,
            'updated_at': self.customer.timestamp_at,
            'company': self.customer.company.encoded,
            'agent_id': self.customer.agent_id,
            'active': self.customer.active,
            'delegation': self.customer.delegation.encoded,
            'external_id': self.customer.external_id.encoded,
        }

        if self.customer.gdpr_updated:
            params['gdpr'] = int(self.customer.gdpr)
            params['gdpr_updated_at'] = self.customer.timestamp_at

        condition = {'unique_id': {'op': '=', 'value': self.customer.customer_id}}
        self.__db.update(self.account_id, self.__table, params=params, conditions=condition)

    def patch(self):
        params = {
            'display_name': self.customer.name,
            'email': self.customer.email,
            'phone': self.customer.phone,
            'updated_at': self.customer.timestamp_at,
            'company': self.customer.company.encoded,
            'agent_id': self.customer.agent_id,
            'delegation': self.customer.delegation.encoded,
            'external_id': self.customer.external_id.encoded
        }

        if self.customer.gdpr_updated:
            params['gdpr'] = int(self.customer.gdpr)
            params['gdpr_updated_at'] = self.customer.timestamp_at

        params = {k: v for k, v in params.items() if v}

        condition = {'unique_id': {'op': '=', 'value': self.customer.customer_id}}
        self.__db.update(self.account_id, self.__table, params=params, conditions=condition)

    def update_last_comment_at(self, unique_id, timestamp):
        params = {
            'last_comment_at': timestamp
        }
        condition = {'unique_id': {'op': '=', 'value': unique_id}}
        self.__db.update(self.account_id, self.__table, params=params, conditions=condition)

    def delete(self):
        condition = {'unique_id': {'op': '=', 'value': self.customer_id}}
        self.__db.delete(self.account_id, self.__table, conditions=condition)

    def filter(self, filter_by, sort=None, order=None, limit=100, page=None, logic_operator='and'):
        conditions = {}
        order_by = None
        if sort and order:
            order_by = [f"{sort_by} {order[i] if i < len(order) else ''}" for i, sort_by in enumerate(sort)]
        for item, value in filter_by.items():
            if item in self.__encoded_fields:
                conditions[
                    f'lower(json_unquote(json_extract(convert(from_base64({item}) using utf8mb4), "$[0]")))'] = {
                    'op': 'like', 'value': f"%{value.lower()}%"}
            else:
                conditions[item] = {'op': 'like', 'value': f"%{value}%"}
        customers = self.__db.select(self.account_id, self.__table, self.__opts, conditions=conditions, order=order_by,
                                     limit=limit, page=page, logic_operator=logic_operator)
        return [CustomerOut(c).data for c in customers]

    def search(self, query, sort=None, order=None, limit=100, page=None):
        order_by = None
        if sort and order:
            order_by = [f"{sort_by} {order[i] if i < len(order) else ''}" for i, sort_by in enumerate(sort)]

        customers = self.__db.select_query(self.account_id, self.__table, self.__opts, query=self.__format_query(query),
                                           order=order_by, limit=limit, page=page)

        return [CustomerOut(c).data for c in customers]

    def count_search(self, query):
        return self.__db.select_query(self.account_id, self.__table, ['count(id)'], query=self.__format_query(query))[
            0].get('count(id)')

    def __format_query(self, query):
        format_query = []
        for q in query:
            if q['type'] == 'condition':
                q = {
                    'type': 'condition',
                    'field': f'lower(json_unquote(json_extract(convert(from_base64({q["field"]}) using utf8mb4), "$[0]")))' if
                    q['field'] in self.__encoded_fields else q['field'],
                    'value': f"%{q['value'].lower()}%",
                    'condition': 'like'
                }
            format_query.append(q)
        return format_query
    
    # Customers
    def list_customers(self, ids=None):
        if ids:
            if len(ids) > 1:
                conditions = {
                    'unique_id': {'op': 'in', 'value': ids}
                }
            else:
                conditions = {
                    'unique_id': {'op': '=', 'value': ids[0]}
                }
        opts = [ 'unique_id', 'agent_id', 'display_name', 'company', 'delegation', 'external_id']
        return self.__db.select(self.account_id, self.__table, opts, conditions)
