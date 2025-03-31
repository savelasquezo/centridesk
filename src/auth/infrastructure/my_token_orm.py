from api.models.accounts.accounts import Accounts
from api.models.token.my_token import MyToken
from api.serializers.token.my_token import MyTokenSerializer


class MyTokenOrm:

    def __init__(self, account_id=None, name=None):
        self.account_id = account_id
        self.name = name

    def create(self):
        account = Accounts.objects.get(unique_id=self.account_id)
        token = MyToken.objects.create(user=account, name=self.name)
        return MyTokenSerializer(token).data

    def get_by_account(self):
        tokens = MyToken.objects.filter(user__unique_id=self.account_id)
        return MyTokenSerializer(tokens, many=True).data
