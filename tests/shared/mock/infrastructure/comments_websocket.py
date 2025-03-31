class CommentsWebsocket:

    def __init__(self, account_id=None, ticket_id=None, ticket_auto_id=None, ticket_subject=None, ticket_status=None,
                 ticket_status_id=None, comment_id=None, comment_text=None, comment_author_id=None,
                 comment_created_at=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.ticket_auto_id = ticket_auto_id
        self.ticket_subject = ticket_subject
        self.ticket_status = ticket_status
        self.ticket_status_id = ticket_status_id
        self.comment_id = comment_id
        self.comment_text = comment_text
        self.comment_author_id = comment_author_id
        self.comment_created_at = comment_created_at

    def send_new(self):
        pass
