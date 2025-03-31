from rest_framework import serializers

from api_centribot.models.accounts.accounts_platform_products import AccountsPlatformProducts


class AccountsPlatformProductsByModel(serializers.ModelSerializer):
    id = serializers.UUIDField(source='account_id')

    class Meta:
        model = AccountsPlatformProducts
        fields = ('id', 'centridesk', 'centripush')
