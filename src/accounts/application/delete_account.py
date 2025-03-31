class DeleteAccount:
    def __init__(self, account_id, accounts_obj, accounts_db_obj):
        self.account_id = account_id
        self.accounts_obj = accounts_obj
        self.accounts_db_obj = accounts_db_obj

    def delete(self):
        self.accounts_obj.account_id = self.account_id
        self.accounts_obj.delete()

        self.accounts_db_obj.account_id = self.account_id
        self.accounts_db_obj.drop_db()
