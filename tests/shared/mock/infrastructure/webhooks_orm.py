from tests.shared.mock.data import MockData


class WebhooksOrm:
    def __init__(self, account_id=None, mock=None):
        self.account_id = account_id
        self.mock = mock or MockData()

    def get_by_account(self):
        output = {}

        for w in self.mock.account_webhooks:
            if w['account_id'] == self.account_id:
                output = self.__format(w)

        return output

    @staticmethod
    def __format(w):
        return {'token': w['token']}
