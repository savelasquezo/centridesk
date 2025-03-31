from src.tickets.application.ticket_get import GetTicket
from src.tickets.domain.ticket_filter import TicketFilter


class FilterTickets:

    def __init__(self, account_id, sort, order, tickets_obj, customers_obj, agents_obj, status_dict, priorities_dict,
                 channels_dict, filters, page=None, page_size=None, logic_operator='and'):
        self.account_id = account_id
        self.filters = filters
        self.sort = sort
        self.order = order
        self.tickets_obj = tickets_obj
        self.customers_obj = customers_obj
        self.agents_obj = agents_obj
        self.status_dict = status_dict
        self.priorities_dict = priorities_dict
        self.channels_dict = channels_dict
        self.page = page
        self.page_size = page_size
        self.logic_operator = logic_operator

    def get(self):
        ticket_filter = TicketFilter(self.filters, self.sort, self.order)

        self.tickets_obj.account_id = self.account_id
        total = self.tickets_obj.count(ticket_filter.filters, self.logic_operator)
        tickets = self.tickets_obj.filter(ticket_filter.filters, ticket_filter.sort, ticket_filter.order,
                                          self.page_size, self.page, self.logic_operator)

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
