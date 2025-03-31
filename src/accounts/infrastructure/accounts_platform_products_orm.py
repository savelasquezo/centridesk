from django.core.exceptions import ObjectDoesNotExist

from api_centribot.models.accounts.accounts_platform_products import AccountsPlatformProducts
from api_centribot.serializers.accounts.accounts_platform_products import AccountsPlatformProductsByModel


class AccountsPlatformProductsOrm:

    def __init__(self, account_id=None):
        self.account_id = account_id

    def get_by_id(self):
        try:
            products = AccountsPlatformProducts.objects.get(account_id=self.account_id)
            product = AccountsPlatformProductsByModel(products).data
        except ObjectDoesNotExist:
            product = None

        return product
