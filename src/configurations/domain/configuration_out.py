from shared.infrastructure.b64 import decode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class ConfigurationOut:

    def __init__(self, info=None, created_at=None, updated_at=None) -> None:
        self.data = {}

        if info:
            self.data = {
                'info': decode_obj(info),
                'created_at': from_timestamp_to_date(created_at),
                'updated_at': from_timestamp_to_date(updated_at),
            }
