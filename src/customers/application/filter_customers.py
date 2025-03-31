from shared.customers.application.format_filter import format_filters
from src.customers.application.ticket_customers import TicketCustomers
from src.customers.domain.customer_filter import CustomerFilter


class FilterCustomers:

    def __init__(self, account_id, customers_obj, sort, order, filters, tickets_obj, status_obj, channels_obj,
                 page=None, page_size=None, logic_operator='and'):
        self.account_id = account_id
        self.filters = filters
        self.sort = sort
        self.order = order
        self.customers_obj = customers_obj
        self.page = page
        self.page_size = page_size
        self.logic_operator = logic_operator
        self.tickets_obj = tickets_obj
        self.status_obj = status_obj
        self.channels_obj = channels_obj

    def get(self):
        self.filters = format_filters(self.filters)

        customer_filter = CustomerFilter(self.filters, self.sort, self.order)

        self.customers_obj.account_id = self.account_id
        total = self.customers_obj.count(customer_filter.filters, self.logic_operator)
        customers = self.customers_obj.filter(customer_filter.filters, customer_filter.sort, customer_filter.order,
                                              self.page_size, self.page, self.logic_operator)
        app_ticket_customers = TicketCustomers(
            customers=customers,
            account_id=self.account_id,
            tickets_obj=self.tickets_obj,
            status_obj=self.status_obj,
            channels_obj=self.channels_obj
        )
        return app_ticket_customers.process(), total
