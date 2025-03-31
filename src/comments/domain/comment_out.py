from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class CommentOut:

    def __init__(self, data):
        self.data = None

        if data:
            self.data = {
                'id': data['unique_id'],
                'text': decode_obj(data['text']),
                'text_json': decode_obj(data['text_json']),
                'attachments': decode_obj(data['attachments']),
                'author_id': data['author_id'],
                'is_agent': data['is_agent'],
                'public': bool(data['public']),
                'ticket_id': data['ticket_id'],
                'created_at': from_timestamp_to_date(data['created_at'])
            }
