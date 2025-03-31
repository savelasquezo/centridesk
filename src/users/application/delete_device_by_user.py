from shared.infrastructure.b64 import encode_obj
from shared.infrastructure.timestamps import get_timestamp


class DeleteUserDeviceByUser:

    def __init__(self, user_id, mobile_id, userstoken_obj):
        self.user_id = user_id
        self.mobile_id = mobile_id
        self.userstoken_obj = userstoken_obj

    def delete(self):
        self.userstoken_obj.centribot_user_id = self.user_id
        usertoken = self.userstoken_obj.get()

        if usertoken:
            mobile_ids = usertoken['mobile_id'] or []
            if self.mobile_id in mobile_ids:
                mobile_ids.remove(self.mobile_id)
                self.userstoken_obj.mobile_id = encode_obj(mobile_ids)
                self.userstoken_obj.updated_at = get_timestamp()
                usertoken = self.userstoken_obj.update_mobile_id_by_user_id()

        return usertoken
