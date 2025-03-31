from rest_framework import serializers

from api.models.users.users_token import UsersToken
from api.serializers.shared.decode_b64 import B64DecodeText


class UsersTokenSerializer(serializers.ModelSerializer):
    mobile_id = B64DecodeText()

    class Meta:
        model = UsersToken
        fields = ('centribot_user_id', 'mobile_id', 'created_at', 'key', 'updated_at')
