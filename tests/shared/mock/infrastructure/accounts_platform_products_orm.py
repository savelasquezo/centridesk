from tests.shared.mock.data import MockData


class AccountsPlatformProductsOrm:

    def __init__(self, account_id=None, mock=None):
        self.account_id = account_id

        self.__mock = mock or MockData()

    def get_by_id(self):
        for app in self.__mock.accounts_platform_products:
            if app['account_id'] == self.account_id:
                return app

        return None
