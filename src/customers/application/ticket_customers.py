class TicketCustomers:

    def __init__(self, customers, account_id, tickets_obj, status_obj, channels_obj):
        self.account_id = account_id
        self.tickets_obj = tickets_obj
        self.status_obj = status_obj
        self.customers = customers
        self.channels_obj = channels_obj

    def process(self):
        filter_customers = []
        if self.customers:
            self.tickets_obj.account_id = self.account_id
            authors = [c['id'] for c in self.customers]

            tickets = self.tickets_obj.get_by_customers(authors, ['created_at desc'])
            status_dict = {s['id']: s['name'] for s in self.status_obj.get_all()}
            channels_dict = {c['id']: c['name'] for c in self.channels_obj.get_all()}

            tc = {}
            # Get all tickets of authors
            for t in tickets:
                if not tc.get(t['author_id']):
                    tc[t['author_id']] = []
                tc[t['author_id']].append(t)

            for c in self.customers:
                customer_tickets = tc.get(c['id'], None)
                status = None
                channel = None
                if customer_tickets:
                    status = status_dict[customer_tickets[0]['status_id']]
                    channel = channels_dict[customer_tickets[0]['channel_id']]
                c['last_ticket_status'] = status
                c['last_ticket_channel'] = channel
                filter_customers.append(c)

        return filter_customers
