from api.tests.shared.mock_data import MockData


class AccountsDatabaseMysql:

    def __init__(self, account_id=None, mock=None):
        self.account_id = account_id
        self.__mock = mock or MockData()

    def check_account_db_exists(self):
        return self.account_id in self.__mock.accounts_databases

    def create_db(self):
        pass

    def drop_db(self):
        pass

    def create_tables(self):
        self.create_customers_table()
        self.create_tickets_table()
        self.create_comments_tables()

    def create_customers_table(self):
        pass

    def create_tickets_table(self):
        pass

    def create_comments_tables(self):
        pass
