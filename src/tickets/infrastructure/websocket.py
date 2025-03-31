from shared.infrastructure.timestamps import from_timestamp_to_date
from src.websocket.infrastructure.websocket_sender import WebsocketSender


class TicketsWebsocket:

    def __init__(self, account_id=None, ticket_id=None, auto_id=None, author_id=None, subject=None, status=None,
                 status_id=None, created_at=None, comment=None, customer_id=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.auto_id = auto_id
        self.author_id = author_id
        self.subject = subject
        self.status = status
        self.status_id = status_id
        self.created_at = created_at
        self.comment = comment

        self.customer_id = customer_id

        self.__ws = WebsocketSender()

    def send_new(self):
        body = {
            'type': 'centridesk',
            'event': 'ticket_created',
            'ticket': {
                'auto_id': self.auto_id,
                'id': self.ticket_id,
                'author_id': self.author_id,
                'subject': self.subject,
                'status': self.status,
                'status_id': self.status_id,
                'created_at': self.created_at
            }
        }

        if self.comment:
            body['comment'] = {
                'id': self.comment.comment_id,
                'comment_id': self.comment.comment_id,
                'author_id': self.comment.author_id,
                'text': self.comment.text,
                'text_json': self.comment.text_json,
                'is_agent': int(self.comment.is_agent),
                'public': self.comment.public,
                'attachments': self.comment.attachments.data if self.comment.attachments else [],
                'created_at': from_timestamp_to_date(self.comment.timestamp)
            }

        self.__send(body)

    def send_updated(self):
        body = {
            'type': 'centridesk',
            'event': 'ticket_updated',
            'ticket': {
                'auto_id': self.auto_id,
                'id': self.ticket_id
            }
        }

        self.__send(body)

    def __send(self, body):
        self.__ws.channel = body['channel'] = self.account_id
        self.__ws.body = body
        self.__ws.send()

        if self.customer_id:
            self.__ws.channel = body['channel'] = f"{self.account_id}_{self.customer_id}"
            self.__ws.body = body
            self.__ws.send()
