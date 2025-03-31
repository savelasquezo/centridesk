from shared.infrastructure.b64 import encode_obj
from src.tickets.domain.ticket_out import TicketOut
from tests.shared.mock.data import MockData


class TicketsMysql:

    def __init__(self, account_id=None, ticket=None, ticket_id=None, mock=None):
        self.account_id = account_id
        self.ticket = ticket
        self.ticket_id = ticket_id

        self.mock = mock or MockData()

    def create(self):
        ticket = {
            'id': len(self.mock.tickets[self.account_id]) + 1,
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
            'created_at': self.ticket.timestamp,
            'updated_at': None,
            'closed_at': None
        }

        self.mock.tickets[self.account_id].append(ticket)

    def get_by_id(self):
        for ticket in self.mock.tickets.get(self.account_id, []):
            if ticket['unique_id'] == self.ticket_id:
                return TicketOut(ticket).data

    def get_all(self, order=None, limit=None, offset=None):
        tickets = [TicketOut(t).data for t in self.mock.tickets.get(self.account_id, [])]
        if order:
            aux = order[0].split(' ')
            tickets.sort(key=lambda x: x[aux[0]], reverse=True if aux[1] == 'desc' else False)
        if limit and offset:
            tickets = tickets[offset:offset + limit]
        return tickets

    def count(self, filter_by=None, logic_operator='and'):
        tickets = self.mock.tickets.get(self.account_id, [])
        if filter_by:
            tickets = []
            for ticket in self.mock.tickets.get(self.account_id, []):
                condition = logic_operator == 'and'
                for item, value in filter_by.items():

                    if logic_operator == 'and':
                        if ticket[item] != value:
                            condition = False
                            break

                    if logic_operator == 'or':
                        if ticket[item] == value:
                            condition = True

                if condition:
                    tickets.append(ticket)
        return len(tickets)

    def get_by_customers(self, author_ids, order=None):
        tickets = [TicketOut(t).data for t in self.mock.tickets.get(self.account_id, [])
                   if t['author_id'] in author_ids]
        if order:
            aux = order[0].split(' ')
            tickets.sort(key=lambda x: x[aux[0]], reverse=True if aux[1] == 'desc' else False)
        return tickets

    def filter(self, filter_by, sort=None, order=None, limit=None, offset=None, logic_operator='and'):
        sort = sort[0] if sort else None
        order = order[0] if order else None
        filtered = []
        for ticket in self.mock.tickets.get(self.account_id, []):
            condition = logic_operator == 'and'
            for item, value in filter_by.items():

                if logic_operator == 'and':
                    if ticket[item] != value:
                        condition = False
                        break

                if logic_operator == 'or':
                    if ticket[item] == value:
                        condition = True

            if condition:
                filtered.append(ticket)

        if sort:
            filtered.sort(reverse=True if order == 'desc' else False, key=lambda t: t[sort])
        if offset and limit:
            filtered = filtered[offset:offset + limit]
        elif limit:
            filtered = filtered[:limit]

        return filtered
