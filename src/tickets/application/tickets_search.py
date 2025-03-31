from src.tickets.application.ticket_get import GetTicket


class SearchTickets:

    def __init__(self, account_id, search, tickets_obj, customers_obj, agents_obj, status_dict, priorities_dict,
                 channels_dict, page=None, page_size=None):
        self.account_id = account_id
        self.search = search
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
        total = self.tickets_obj.count_search(self.search.query)
        tickets = self.tickets_obj.search(self.search.query, self.search.sort, self.search.order, self.page_size,
                                          self.page)

        output = []
        for ticket in tickets:
            getter = GetTicket(
                account_id=self.account_id,
                ticket_id=ticket['unique_id'],
                tickets_obj=self.tickets_obj,
                customers_obj=self.customers_obj,
                agents_obj=self.agents_obj,
                status_dict=self.status_dict,
                priorities_dict=self.priorities_dict,
                channels_dict=self.channels_dict
            )
            output.append(getter.get())

        return output, total
