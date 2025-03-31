from django.core.exceptions import ObjectDoesNotExist

from api.models.accounts.accounts import Accounts
from api.serializers.accounts.accounts import AccountSerializer
from shared.exceptions.not_found import NotFound


class AccountsOrm:

    def __init__(self, account_id=None, name=None, active=True):
        self.account_id = account_id
        self.name = name
        self.active = active

    def create(self):
        account = Accounts.objects.create(unique_id=self.account_id, name=self.name, is_active=self.active)
        return AccountSerializer(account).data

    def get(self):
        try:
            account = Accounts.objects.get(unique_id=self.account_id)

        except ObjectDoesNotExist:
            raise NotFound('account')

        return AccountSerializer(account).data

    def check_exists(self):
        return Accounts.objects.filter(unique_id=self.account_id).exists()

    def delete(self):
        try:
            account = Accounts.objects.get(unique_id=self.account_id)
            account.delete()

        except ObjectDoesNotExist:
            raise NotFound('account')
