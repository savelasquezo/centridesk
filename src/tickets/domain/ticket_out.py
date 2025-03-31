from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class TicketOut:

    def __init__(self, data):
        self.data = None

        if data:
            self.data = {
                'id': data['unique_id'],
                'auto_id': data['id'],
                'subject': decode_obj(data['title']),
                'status_id': data['status_id'],
                'priority_id': data['priority_id'],
                'author_id': data['author_id'],
                'is_agent': bool(data['is_agent']),
                'assignee_id': data['assignee_id'],
                'channel_id': data['channel_id'],
                'external_id': data['external_id'],
                'centribot_project_id': data['centribot_project_id'],
                'centribot_channel_id': data['centribot_channel_id'],
                'tags': decode_obj(data['tags']),
                'created_at': from_timestamp_to_date(data['created_at']),
                'updated_at': from_timestamp_to_date(data['updated_at']),
                'closed_at': from_timestamp_to_date(data['closed_at'])
            }
