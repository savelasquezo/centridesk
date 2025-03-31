from src.tickets.application.ticket_get_add_info import add_ticket_info


class GetTickets:

    def __init__(self, account_id, tickets_obj, customers_obj, agents_obj, status_dict, priorities_dict, channels_dict,
                 page=None, page_size=None):
        self.account_id = account_id
        self.tickets_obj = tickets_obj
        self.customers_obj = customers_obj
        self.agents_obj = agents_obj
        self.status_dict = status_dict
        self.priorities_dict = priorities_dict
        self.channels_dict = channels_dict
        self.page = page
        self.page_size = page_size

    def get(self):
        self.tickets_obj.account_id = self.account_id
        total = self.tickets_obj.count()
        tickets = self.tickets_obj.get_all(limit=self.page_size, page=self.page)

        for t in tickets:
            add_ticket_info(self.account_id, t, self.customers_obj, self.agents_obj, self.status_dict,
                            self.priorities_dict, self.channels_dict)

        return tickets, total
