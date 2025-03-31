from shared.infrastructure.timestamps import get_timestamp
from shared.value_objects.mobile_id import MobileId


class UsersDeviceEditIn:

    def __init__(self, mobile_id):
        self.mobile_id = mobile_id
        self.timestamp_at = get_timestamp()

    @property
    def mobile_id(self):
        return self.__mobile_id

    @mobile_id.setter
    def mobile_id(self, mobile_id):
        self.__mobile_id = MobileId(mobile_id).mobile_id
