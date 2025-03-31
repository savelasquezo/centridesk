from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class CustomerOut:

    def __init__(self, customer):
        self.data = customer
        if self.data:
            self.data = {
                'id': self.data['unique_id'],
                'agent_id': self.data.get('agent_id', None),
                'name': self.data['display_name'],
                'email': self.data['email'],
                'phone': self.data['phone'],
                'centribot_external_id': self.data['centribot_external_id'],
                'company': decode_obj(self.data.get('company', None)),
                'delegation': decode_obj(self.data.get('delegation', None)),
                'external_id': decode_obj(self.data.get('external_id', None)),
                'gdpr': bool(self.data['gdpr']),
                'gdpr_updated_at': from_timestamp_to_date(self.data['gdpr_updated_at']),
                'last_comment_at': from_timestamp_to_date(self.data['last_comment_at']),
                'created_at': from_timestamp_to_date(self.data['created_at']),
                'updated_at': from_timestamp_to_date(self.data['updated_at']),
                'active': bool(self.data['active'])
            }
