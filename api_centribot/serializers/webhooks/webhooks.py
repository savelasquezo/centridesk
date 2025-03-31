from rest_framework import serializers

from api_centribot.models.webhooks.webhooks import Webhooks


class WebhooksSerializerByModel(serializers.ModelSerializer):
    class Meta:
        model = Webhooks
        fields = ('token',)
