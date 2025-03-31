import binascii
import os

from django.core.exceptions import ObjectDoesNotExist

from api.models.users.users_token import UsersToken
from api.serializers.users.users_token import UsersTokenSerializer


class UsersTokenOrm:

    def __init__(self, centribot_user_id=None, mobile_id=None, created_at=None, key=None, updated_at=None):
        self.centribot_user_id = centribot_user_id
        self.mobile_id = mobile_id
        self.created_at = created_at
        self.key = key
        self.updated_at = updated_at

    def create(self):
        access = UsersToken.objects.create(
            centribot_user_id=self.centribot_user_id,
            mobile_id=self.mobile_id,
            key=binascii.hexlify(os.urandom(20)).decode(),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
        return UsersTokenSerializer(access).data

    def get(self):
        try:
            access = UsersToken.objects.get(centribot_user_id=self.centribot_user_id)
            return UsersTokenSerializer(access).data
        except ObjectDoesNotExist:
            return None

    def get_by_key(self):
        try:
            access = UsersToken.objects.get(key=self.key)
            return UsersTokenSerializer(access).data
        except ObjectDoesNotExist:
            return None

    def update_mobile_id_by_key(self):
        try:
            access = UsersToken.objects.get(key=self.key)

            access.mobile_id = self.mobile_id
            access.updated_at = self.updated_at
            access.save()

            return UsersTokenSerializer(access).data
        except ObjectDoesNotExist:
            return None

    def update_mobile_id_by_user_id(self):
        try:
            access = UsersToken.objects.get(centribot_user_id=self.centribot_user_id)

            access.mobile_id = self.mobile_id
            access.updated_at = self.updated_at
            access.save()

            return UsersTokenSerializer(access).data
        except ObjectDoesNotExist:
            return None
