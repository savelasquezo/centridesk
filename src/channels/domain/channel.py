from shared.infrastructure.timestamps import from_timestamp_to_date


class Channel:

    def __init__(self, data):
        self.data = None

        if data:
            self.data = {
                'id': data['unique_id'],
                'name': data['name'],
                'platform': data['platform'],
                'active': bool(data['active']),
                'created_at': from_timestamp_to_date(data['created_at'])
            }
