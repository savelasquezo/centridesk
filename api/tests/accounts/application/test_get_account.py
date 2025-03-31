from django.test import SimpleTestCase

from src.accounts.application.get_account import GetAccount
from api.tests.shared.mock_data import MockData
from api.tests.shared.mock_infrastructure.accounts.accounts_orm import AccountsOrm
from api.tests.shared.mock_infrastructure.auth.my_token_orm import MyTokenOrm
from shared.exceptions.not_found import NotFound


class TestGetAccount(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        app = GetAccount(
            account_id=self.__mock.account_id1,
            accounts_obj=AccountsOrm(),
            token_obj=MyTokenOrm()
        )

        expected = {
            'id': self.__mock.account_id1,
            'name': self.__mock.account_id1,
            'token': [{'name': 'centribot', 'key': self.__mock.token1}],
            'active': True
        }

        self.assertEqual(app.get(), expected)

    def test_not_found(self):
        try:
            app = GetAccount(
                account_id=self.__mock.account_not_found,
                accounts_obj=AccountsOrm(),
                token_obj=MyTokenOrm()
            )
            app.get()

        except NotFound:
            self.assertRaisesMessage(NotFound, 'Account not found')
