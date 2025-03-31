from src.comments.domain.comments_filter import CommentsFilter


class GetComments:

    def __init__(self, account_id, ticket_id, comments_obj, tickets_obj, sort, order, page=None, page_size=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.comments_obj = comments_obj
        self.tickets_obj = tickets_obj
        self.sort = sort
        self.order = order
        self.page = page
        self.page_size = page_size

    def get(self):
        self.tickets_obj.account_id = self.comments_obj.account_id = self.account_id

        self.tickets_obj.ticket_id = self.ticket_id
        self.tickets_obj.get_by_id()

        comments_filter = CommentsFilter(self.sort, self.order)

        self.comments_obj.ticket_id = self.ticket_id
        total = self.comments_obj.count_by_ticket()
        return self.comments_obj.get_by_ticket(comments_filter.sort, comments_filter.order, self.page_size,
                                               self.page), total
