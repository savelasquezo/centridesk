from shared.exceptions.generic import GenericException


class SetUpAccount:

    def __init__(self, account_id, setup_obj, accounts_obj, token_obj):
        self.account_id = account_id
        self.setup_obj = setup_obj
        self.accounts_obj = accounts_obj
        self.token_obj = token_obj

        self.rollback_db = False
        self.rollback_account = False

    def set_up(self):
        # check the account does not exists
        self.accounts_obj.account_id = self.account_id
        if self.accounts_obj.check_exists():
            raise GenericException('account already exists')

        # check the database is not created
        self.setup_obj.account_id = self.account_id
        if self.setup_obj.check_account_db_exists():
            raise GenericException('account db already exists')

        try:
            # create database and tables
            self.setup_obj.create_db()
            self.rollback_db = True

            self.setup_obj.create_tables()

            # create account
            self.accounts_obj.account_id = self.account_id
            self.accounts_obj.name = self.account_id
            account = self.accounts_obj.create()
            self.rollback_account = True

            # create Centribot token to this account
            self.token_obj.account_id = self.account_id
            self.token_obj.name = 'centribot'
            account['token'] = self.token_obj.create()

            return account

        except Exception as ex:
            try:
                if self.rollback_db:
                    self.setup_obj.drop_db()

                if self.rollback_account:
                    self.accounts_obj.delete()

            except Exception as ex:
                raise Exception(f"Rollback Error: {ex}")

            raise Exception(f"{ex}")
