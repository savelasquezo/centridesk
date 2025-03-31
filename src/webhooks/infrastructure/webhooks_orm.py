from django.core.exceptions import ObjectDoesNotExist

from api_centribot.models.webhooks import Webhooks
from api_centribot.serializers.webhooks.webhooks import WebhooksSerializerByModel


class WebhooksOrm:
    def __init__(self, account_id=None):
        self.account_id = account_id

    def get_by_account(self):
        try:
            webhook = Webhooks.objects.get(account_id=self.account_id)
            output = WebhooksSerializerByModel(webhook).data
        except ObjectDoesNotExist:
            output = {}

        return output
