class GetComment:

    def __init__(self, account_id, ticket_id, comment_id, comments_obj):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.comment_id = comment_id
        self.comments_obj = comments_obj

    def get(self):
        self.comments_obj.account_id = self.account_id
        self.comments_obj.ticket_id = self.ticket_id
        self.comments_obj.comment_id = self.comment_id
        return self.comments_obj.get_by_id()
