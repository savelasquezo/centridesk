from api.tests.shared.mock_data import MockData
from shared.exceptions.not_found import NotFound


class AccountsOrm:

    def __init__(self, account_id=None, name=None, active=True, mock=None):
        self.account_id = account_id
        self.name = name
        self.active = active
        self.__mock = mock or MockData()

    def create(self):
        account = {'unique_id': self.account_id, 'name': self.name, 'active': self.active}
        self.__mock.accounts.append(account)
        return self.__format(account)

    def get(self):
        output = None
        for account in self.__mock.accounts:
            if account['unique_id'] == self.account_id:
                output = self.__format(account)
                break

        if not output:
            raise NotFound('account')

        return output

    def check_exists(self):
        output = False
        for account in self.__mock.accounts:
            if account['unique_id'] == self.account_id:
                output = True
                break

        return output

    def delete(self):
        found = False
        for account in self.__mock.accounts:
            if account['unique_id'] == self.account_id:
                self.__mock.accounts.remove(account)
                found = True
                break

        if not found:
            raise NotFound('account')

    @staticmethod
    def __format(account):
        if account:
            account = {
                'id': account['unique_id'],
                'name': account['name'],
                'active': account['active']
            }

        return account
