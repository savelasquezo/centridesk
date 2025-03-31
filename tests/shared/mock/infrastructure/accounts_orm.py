from tests.shared.mock.data import MockData


class AccountsOrm:

    def __init__(self, account_id=None, name=None, active=True, mock=None):
        self.account_id = account_id
        self.name = name
        self.active = active

        self.__mock = mock or MockData()

    def check_exists(self):
        return self.account_id in self.__mock.accounts
