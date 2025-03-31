from django.test import TestCase

from src.auth.infrastructure.my_token_orm import MyTokenOrm
from api.tests.shared.database import accounts, token
from api.tests.shared.mock_data import MockData
from shared.exceptions.not_found import NotFound


class TestMyTokenOrm(TestCase):

    @classmethod
    def setUpTestData(cls):
        mock = MockData()

        accounts.create_many_by_id(mock, [mock.account_id1, mock.account_id2])
        token.create(mock.account_id2, 'Centribot')
        token.create(mock.account_id2, 'Testing')

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_create_ok(self):
        token_obj = MyTokenOrm(account_id=self.__mock.account_id1, name='Centribot')
        result = token_obj.create()

        self.assertEqual(result['name'], 'Centribot')
        self.assertTrue('key' in result.keys())

    def test_get_not_found(self):
        try:
            token_obj = MyTokenOrm(account_id=self.__mock.account_not_found)
            token_obj.get_by_account()
        except NotFound:
            self.assertRaisesMessage(NotFound, 'Account not found')

    def test_get_many(self):
        token_obj = MyTokenOrm(account_id=self.__mock.account_id2)
        result = token_obj.get_by_account()

        expected = [{'name': t.name, 'key': t.key} for t in token.get(self.__mock.account_id2)]

        self.assertEqual(result, expected)
