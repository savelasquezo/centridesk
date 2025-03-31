from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class AgentOut:

    def __init__(self, data):
        self.data = None

        if data:
            self.data = {
                'id': data['unique_id'],
                'name': f"{data['first_name']} {data['last_name']}",
                'email': data['email'],
                'lang': data['lang'],
                'active': bool(data['is_active']),
                'created_at': from_timestamp_to_date(data['created_at']),
                'updated_at': from_timestamp_to_date(data['updated_at']),
                'deactivated_at': from_timestamp_to_date(data['deactivated_at']),
                'desk': decode_obj(data.get('desk', None))
            }
