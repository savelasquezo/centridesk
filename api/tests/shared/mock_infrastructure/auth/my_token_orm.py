from api.tests.shared.mock_data import MockData


class MyTokenOrm:

    def __init__(self, account_id=None, name=None, mock=None):
        self.account_id = account_id
        self.name = name
        self.__mock = mock or MockData()

    def create(self):
        token = {'name': self.name, 'key': self.__mock.new_token, 'account_id': self.account_id}
        self.__mock.my_tokens.append(token)
        return self.__format(token)

    def get_by_account(self):
        return [self.__format(item) for item in self.__mock.my_tokens if item['account_id'] == self.account_id]

    @staticmethod
    def __format(token):
        if token:
            token = {
                'name': token['name'],
                'key': token['key']
            }

        return token
