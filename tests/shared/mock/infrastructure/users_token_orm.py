from django.core.exceptions import ObjectDoesNotExist

from api.serializers.users.users_token import UsersTokenSerializer
from tests.shared.mock.data import MockData


class UsersTokenOrm:

    def __init__(self, centribot_user_id=None, mobile_id=None, created_at=None, key=None, updated_at=None, mock=None):
        self.centribot_user_id = centribot_user_id
        self.mobile_id = mobile_id
        self.created_at = created_at
        self.key = key
        self.updated_at = updated_at

        self.__mock = mock or MockData()

    def get(self):
        try:
            for user_token in self.__mock.users_tokens:
                if user_token['centribot_user_id'] == self.centribot_user_id:
                    return UsersTokenSerializer(user_token).data
        except ObjectDoesNotExist:
            return None

    def get_by_key(self):
        try:
            for user_token in self.__mock.users_tokens:
                if user_token['key'] == self.key:
                    return UsersTokenSerializer(user_token).data
        except ObjectDoesNotExist:
            return None

    def update_mobile_id_by_user_id(self):
        try:
            for user_token in self.__mock.users_tokens:
                if user_token['centribot_user_id'] == self.centribot_user_id:
                    user_token['mobile_id'] = self.mobile_id
                    return UsersTokenSerializer(user_token).data
        except ObjectDoesNotExist:
            return None

    def update_mobile_id_by_key(self):
        try:
            for user_token in self.__mock.users_tokens:
                if user_token['key'] == self.key:
                    user_token['mobile_id'] = self.mobile_id
                    return UsersTokenSerializer(user_token).data
        except ObjectDoesNotExist:
            return None
