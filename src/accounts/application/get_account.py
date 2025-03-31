class GetAccount:
    def __init__(self, account_id, accounts_obj, token_obj):
        self.account_id = account_id
        self.accounts_obj = accounts_obj
        self.token_obj = token_obj

    def get(self):
        self.accounts_obj.account_id = self.account_id
        account = self.accounts_obj.get()

        self.token_obj.account_id = self.account_id
        account['token'] = self.token_obj.get_by_account()

        return account
