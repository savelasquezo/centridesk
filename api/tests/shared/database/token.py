from api.models.accounts.accounts import Accounts
from api.models.token.my_token import MyToken


def create(account_id, name):
    account = Accounts.objects.get(unique_id=account_id)
    MyToken.objects.create(user=account, name=name)


def get(account_id):
    return MyToken.objects.filter(user__unique_id=account_id)
