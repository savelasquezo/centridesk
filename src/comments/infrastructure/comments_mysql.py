from shared.exceptions.not_found import NotFound
from shared.infrastructure.b64 import encode_obj
from shared.mysql.infrastructure.mysql_methods import MysqlMethods
from src.comments.domain.comment_out import CommentOut


class CommentsMysql:

    def __init__(self, account_id=None, comment=None, comment_id=None, ticket_id=None):
        self.__db = MysqlMethods('centridesk')
        self.__table = 'comments'
        self.account_id = account_id
        self.comment = comment
        self.comment_id = comment_id
        self.ticket_id = ticket_id

        self.__opts = ['unique_id', 'text', 'text_json', 'attachments', 'author_id', 'is_agent', 'public', 'ticket_id',
                       'created_at']

    def create(self):
        params = {
            'unique_id': self.comment.comment_id,
            'text': encode_obj(self.comment.text),
            'text_json': encode_obj(self.comment.text_json),
            'attachments': self.comment.attachments.data_encoded if self.comment.attachments else None,
            'author_id': self.comment.author_id,
            'is_agent': self.comment.is_agent,
            'public': self.comment.public,
            'ticket_id': self.comment.ticket_id,
            'created_at': self.comment.timestamp
        }

        self.__db.insert(self.account_id, self.__table, params=params)

    def get_by_id(self):
        conditions = {
            'unique_id': {'op': '=', 'value': self.comment_id},
            'ticket_id': {'op': '=', 'value': self.ticket_id}
        }

        comment = self.__db.select_one(self.account_id, self.__table, self.__opts, conditions)

        if not comment:
            raise NotFound('comment')

        return CommentOut(comment).data

    def get_by_ticket(self, sort=None, order=None, limit=None, page=None):
        conditions = {
            'ticket_id': {'op': '=', 'value': self.ticket_id}
        }
        order_by = [f"{sort}{f' {order}' if order else ''}"] if sort else []

        comments = self.__db.select(self.account_id, self.__table, self.__opts, conditions, order=order_by, limit=limit,
                                    page=page)

        return [CommentOut(c).data for c in comments]

    def count_by_ticket(self):
        conditions = {
            'ticket_id': {'op': '=', 'value': self.ticket_id}
        }
        return self.__db.select(self.account_id, self.__table, ['count(id)'], conditions=conditions)[0].get('count(id)')
    
    # Comments
    def list_comments(self, from_filter, to_filter, is_agent=1):
        conditions = {
            'from_unixtime(created_at, "%Y-%m-%d")': {'op': '>=', 'value': from_filter},
            'from_unixtime(created_at, "%Y-%m-%d") ': {'op': '<=', 'value': to_filter},
            'is_agent': {'op': '=', 'value': is_agent}
        }
        opts = ['unique_id', 'author_id', 'from_unixtime(created_at, "%Y-%m-%d") as created_at']
        return self.__db.select(self.account_id, self.__table, opts, conditions)