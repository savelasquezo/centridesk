from shared.exceptions.not_found import NotFound
from shared.infrastructure.b64 import encode_obj
from src.comments.domain.comment_out import CommentOut
from tests.shared.mock.data import MockData


class CommentsMysql:

    def __init__(self, account_id=None, comment=None, comment_id=None, ticket_id=None, mock=None):
        self.account_id = account_id
        self.comment = comment
        self.comment_id = comment_id
        self.ticket_id = ticket_id

        self.mock = mock or MockData()

    def create(self):
        comment = {
            'id': len(self.mock.comments[self.account_id]) + 1,
            'unique_id': self.comment.comment_id,
            'text': encode_obj(self.comment.text),
            'text_json': encode_obj(self.comment.text_json),
            'attachments': self.comment.attachments.data_encoded if self.comment.attachments else None,
            'author_id': self.comment.author_id,
            'is_agent': int(self.comment.is_agent),
            'public': self.comment.public,
            'ticket_id': self.comment.ticket_id,
            'created_at': self.comment.timestamp
        }

        self.mock.comments[self.account_id].append(comment)

    def get_by_id(self):
        for comment in self.mock.comments.get(self.account_id, []):
            if comment['unique_id'] == self.comment_id and comment['ticket_id'] == self.ticket_id:
                return CommentOut(comment).data

        raise NotFound('comment')

    def get_by_ticket(self, sort=None, order=None, limit=None, offset=None):
        comments = self.mock.comments.get(self.account_id, [])
        comments = [c for c in comments if c['ticket_id'] == self.ticket_id]
        if sort:
            comments.sort(reverse=True if order == 'desc' else False, key=lambda c: c[sort])
        if offset and limit:
            comments = comments[offset:offset + limit]
        elif limit:
            comments = comments[:limit]
        return [CommentOut(c).data for c in comments]

    def count_by_ticket(self):
        comments = self.mock.comments.get(self.account_id, [])
        return len([c for c in comments if c['ticket_id'] == self.ticket_id])
