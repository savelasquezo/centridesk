from src.websocket.infrastructure.websocket_sender import WebsocketSender


class CommentsWebsocket:

    def __init__(self, account_id=None, ticket_id=None, ticket_auto_id=None, ticket_subject=None, ticket_status=None,
                 ticket_status_id=None, comment_id=None, comment_text=None, comment_author_id=None,
                 comment_created_at=None, comment_is_agent=None, comment_public=None, ticket_customer_id=None,
                 comment_attachments=None, text_json=None):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.ticket_auto_id = ticket_auto_id
        self.ticket_subject = ticket_subject
        self.ticket_status = ticket_status
        self.ticket_status_id = ticket_status_id
        self.ticket_customer_id = ticket_customer_id
        self.comment_id = comment_id
        self.comment_text = comment_text
        self.comment_text_json = text_json
        self.comment_author_id = comment_author_id
        self.comment_is_agent = comment_is_agent
        self.comment_public = comment_public
        self.comment_created_at = comment_created_at
        self.comment_attachments = comment_attachments

        self.__ws = WebsocketSender()

    def send_new(self):
        body = {
            'type': 'centridesk',
            'event': 'comment_added',
            'ticket': {
                'auto_id': self.ticket_auto_id,
                'id': self.ticket_id,
                'subject': self.ticket_subject,
                'status': self.ticket_status,
                'status_id': self.ticket_status_id
            },
            'comment': {
                'id': self.comment_id,
                'comment_id': self.comment_id,
                'author_id': self.comment_author_id,
                'text': self.comment_text,
                'text_json': self.comment_text_json,
                'is_agent': self.comment_is_agent,
                'public': self.comment_public,
                'attachments': self.comment_attachments,
                'created_at': self.comment_created_at
            }
        }

        self.__send(body)

    def __send(self, body):
        self.__ws.channel = body['channel'] = self.account_id
        self.__ws.body = body
        self.__ws.send()

        if self.ticket_customer_id:
            self.__ws.channel = body['channel'] = f"{self.account_id}_{self.ticket_customer_id}"
            self.__ws.body = body
            self.__ws.send()