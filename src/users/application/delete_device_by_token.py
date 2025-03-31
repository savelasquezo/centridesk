from shared.infrastructure.b64 import encode_obj


class DeleteUserDeviceByKey:

    def __init__(self, key, user_device, userstoken_obj):
        self.key = key
        self.user_device = user_device
        self.userstoken_obj = userstoken_obj

    def delete(self):
        self.userstoken_obj.key = self.key
        usertoken = self.userstoken_obj.get_by_key()

        if usertoken:
            mobile_ids = usertoken['mobile_id'] or []
            if self.user_device.mobile_id in mobile_ids:
                mobile_ids.remove(self.user_device.mobile_id)
                self.userstoken_obj.mobile_id = encode_obj(mobile_ids)
                self.userstoken_obj.updated_at = self.user_device.timestamp_at
                usertoken = self.userstoken_obj.update_mobile_id_by_key()

        return usertoken
