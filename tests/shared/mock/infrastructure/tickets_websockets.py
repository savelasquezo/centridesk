class TicketsWebsocket:
    def __init__(self, account_id=None, ticket_id=None, auto_id=None, author_id=None, subject=None, status=None,
                 status_id=None, created_at=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.auto_id = auto_id
        self.author_id = author_id
        self.subject = subject
        self.status = status
        self.status_id = status_id
        self.created_at = created_at

    def send_new(self):
        pass

    def send_updated(self):
        pass

    def __send(self, body):
        pass
