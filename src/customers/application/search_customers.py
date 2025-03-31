from src.customers.application.ticket_customers import TicketCustomers


class SearchCustomers:

    def __init__(self, account_id, customers_obj, search, tickets_obj, status_obj, channels_obj, page=None,
                 page_size=None):
        self.account_id = account_id
        self.search = search
        self.customers_obj = customers_obj
        self.page = page
        self.page_size = page_size
        self.tickets_obj = tickets_obj
        self.status_obj = status_obj
        self.channels_obj = channels_obj

    def get(self):
        self.customers_obj.account_id = self.account_id
        total = self.customers_obj.count_search(self.search.query)
        customers = self.customers_obj.search(self.search.query, self.search.sort, self.search.order, self.page_size,
                                              self.page)

        app_ticket_customers = TicketCustomers(
            customers=customers,
            account_id=self.account_id,
            tickets_obj=self.tickets_obj,
            status_obj=self.status_obj,
            channels_obj=self.channels_obj
        )

        return app_ticket_customers.process(), total
