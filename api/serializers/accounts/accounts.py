from rest_framework import serializers

from api.models.accounts.accounts import Accounts


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='unique_id')
    active = serializers.BooleanField(source='is_active')

    class Meta:
        model = Accounts
        fields = ('id', 'name', 'active')
