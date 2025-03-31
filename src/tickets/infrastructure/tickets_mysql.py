from shared.exceptions.not_found import NotFound
from shared.infrastructure.b64 import encode_obj
from shared.mysql.infrastructure.mysql_methods import MysqlMethods
from src.tickets.domain.ticket_out import TicketOut


class TicketsMysql:

    def __init__(self, account_id=None, ticket=None, ticket_id=None):
        self.__db = MysqlMethods('centridesk')
        self.__table = 'tickets'
        self.account_id = account_id
        self.ticket = ticket
        self.ticket_id = ticket_id

        self.__opts = ['id', 'unique_id', 'title', 'status_id', 'priority_id', 'author_id', 'is_agent', 'assignee_id',
                       'channel_id', 'external_id', 'centribot_project_id', 'centribot_channel_id', 'tags',
                       'created_at', 'updated_at', 'closed_at']

    def create(self):
        params = {
            'unique_id': self.ticket.ticket_id,
            'title': encode_obj(self.ticket.subject),
            'status_id': self.ticket.status_id,
            'priority_id': self.ticket.priority_id,
            'author_id': self.ticket.author_id,
            'is_agent': self.ticket.is_agent,
            'assignee_id': self.ticket.assignee_id,
            'channel_id': self.ticket.channel_id,
            'external_id': self.ticket.external_id,
            'centribot_project_id': self.ticket.centribot_project_id,
            'centribot_channel_id': self.ticket.centribot_channel_id,
            'tags': encode_obj(self.ticket.tags),
            'created_at': self.ticket.timestamp
        }

        self.__db.insert(self.account_id, self.__table, params=params)

    def get_by_id(self):
        conditions = {'unique_id': {'op': '=', 'value': self.ticket_id}}
        ticket = self.__db.select_one(self.account_id, self.__table, self.__opts, conditions)

        if not ticket:
            raise NotFound('ticket')

        return TicketOut(ticket).data

    def get_all(self, order=None, limit=None, page=None):
        tickets = self.__db.select(self.account_id, self.__table, self.__opts, order=order, limit=limit, page=page)
        return [TicketOut(t).data for t in tickets]

    def count(self, filter_by=None, logic_operator='and'):
        conditions = {}
        if filter_by:
            for item, value in filter_by.items():
                conditions[item] = {'op': '=', 'value': value}
        return self.__db.select(self.account_id, self.__table, ['count(id)'], conditions=conditions,
                                logic_operator=logic_operator)[0].get('count(id)')

    def get_by_customers(self, author_ids, order=None):
        conditions = {'author_id': {'op': 'in', 'value': tuple(author_ids)}}
        tickets = self.__db.select(self.account_id, self.__table, self.__opts, conditions, order=order)
        return [TicketOut(t).data for t in tickets]

    def update(self):
        params = {
            'status_id': self.ticket.status_id,
            'priority_id': self.ticket.priority_id,
            'assignee_id': self.ticket.assignee_id,
            'external_id': self.ticket.external_id,
            'tags': encode_obj(self.ticket.tags),
            'updated_at': self.ticket.timestamp
        }

        conditions = {'unique_id': {'op': '=', 'value': self.ticket_id}}
        self.__db.update(self.account_id, self.__table, params, conditions)

    def filter(self, filter_by, sort=None, order=None, limit=None, page=None, logic_operator='and'):
        conditions = {}
        order_by = [f"{sort_by} {order[i] if i < len(order) else ''}" for i, sort_by in enumerate(sort)]
        for item, value in filter_by.items():
            conditions[item] = {'op': '=', 'value': value}

        return self.__db.select(self.account_id, self.__table, self.__opts, conditions=conditions, order=order_by,
                                limit=limit, page=page, logic_operator=logic_operator)

    def search(self, query, sort=None, order=None, limit=None, page=None):
        order_by = [f"{sort_by} {order[i] if i < len(order) else ''}" for i, sort_by in enumerate(sort)]

        return self.__db.select_query(self.account_id, self.__table, self.__opts, query=query, order=order_by,
                                      limit=limit, page=page)

    def count_search(self, query):
        return self.__db.select_query(self.account_id, self.__table, ['count(id)'], query=query)[0].get('count(id)')
    
    # Tickets
    def list_tickets(self, from_filter, to_filter):
        conditions = {
            'from_unixtime(created_at, "%Y-%m-%d")': {'op': '>=', 'value': from_filter},
            'from_unixtime(created_at, "%Y-%m-%d") ': {'op': '<=', 'value': to_filter},
        }
        opts = ['unique_id', 'assignee_id', 'author_id', 'from_unixtime(created_at, "%Y-%m-%d") as created_at']
        
        return self.__db.select(self.account_id, self.__table, opts, conditions)
