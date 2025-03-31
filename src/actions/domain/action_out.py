from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class ActionOut:

    def __init__(self, data):
        self.data = None

        if data:
            self.data = {
                'id': data['unique_id'],
                'action': data['action'],
                'requester_id': data['requester_id'],
                'pending': bool(data['pending']),
                'in_progress': bool(data['in_progress']),
                'result': data['result'],
                'error': decode_obj(data['error']),
                'info': decode_obj(data['info']),
                'created_at': from_timestamp_to_date(data['created_at']),
                'initiated_at': from_timestamp_to_date(data['initiated_at']),
                'finished_at': from_timestamp_to_date(data['finished_at'])
            }
