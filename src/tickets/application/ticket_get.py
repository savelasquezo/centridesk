from src.tickets.application.ticket_get_add_info import add_ticket_info


class GetTicket:

    def __init__(self, account_id, ticket_id, tickets_obj, customers_obj, agents_obj, status_dict=None,
                 priorities_dict=None, channels_dict=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.tickets_obj = tickets_obj
        self.customers_obj = customers_obj
        self.agents_obj = agents_obj
        self.status_dict = status_dict
        self.priorities_dict = priorities_dict
        self.channels_dict = channels_dict

    def get(self):
        self.tickets_obj.account_id = self.account_id
        self.tickets_obj.ticket_id = self.ticket_id
        ticket = self.tickets_obj.get_by_id()

        return add_ticket_info(self.account_id, ticket, self.customers_obj, self.agents_obj, self.status_dict,
                               self.priorities_dict, self.channels_dict)
