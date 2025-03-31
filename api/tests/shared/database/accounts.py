from api.models.accounts.accounts import Accounts
from api.tests.shared.mock_data import MockData


def create_by_id(mock: MockData, account_id):
    for account in mock.accounts:
        if account['unique_id'] == account_id:
            __create(account)
            break


def create_many_by_id(mock, accounts):
    for account in mock.accounts:
        if account['unique_id'] in accounts:
            __create(account)


def __create(account):
    Accounts.objects.create(
        unique_id=account['unique_id'],
        name=account['name'],
        is_active=account['active']
    )
