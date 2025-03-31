from django.test import SimpleTestCase

from src.accounts.application.setup_account import SetUpAccount
from api.tests.shared.mock_data import MockData
from api.tests.shared.mock_infrastructure.accounts.accounts_database_mysql import AccountsDatabaseMysql
from api.tests.shared.mock_infrastructure.accounts.accounts_orm import AccountsOrm
from api.tests.shared.mock_infrastructure.auth.my_token_orm import MyTokenOrm
from shared.exceptions.generic import GenericException


class TestSetUpAccount(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        app = SetUpAccount(
            account_id=self.__mock.account_not_found,
            setup_obj=AccountsDatabaseMysql(),
            accounts_obj=AccountsOrm(),
            token_obj=MyTokenOrm()
        )

        expected = {
            'id': self.__mock.account_not_found,
            'name': self.__mock.account_not_found,
            'token': {'name': 'centribot', 'key': self.__mock.new_token},
            'active': True
        }

        self.assertEqual(app.set_up(), expected)

    def test_account_already_exists(self):
        try:
            app = SetUpAccount(
                account_id=self.__mock.account_id1,
                setup_obj=AccountsDatabaseMysql(),
                accounts_obj=AccountsOrm(),
                token_obj=MyTokenOrm()
            )
            app.set_up()

        except GenericException:
            self.assertRaisesMessage(GenericException, 'Account already exists')
