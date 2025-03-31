from django.test import SimpleTestCase

from src.accounts.application.delete_account import DeleteAccount
from api.tests.shared.mock_data import MockData
from api.tests.shared.mock_infrastructure.accounts.accounts_database_mysql import AccountsDatabaseMysql
from api.tests.shared.mock_infrastructure.accounts.accounts_orm import AccountsOrm
from shared.exceptions.not_found import NotFound


class TestDeleteAccount(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        app = DeleteAccount(
            account_id=self.__mock.account_id1,
            accounts_obj=AccountsOrm(),
            accounts_db_obj=AccountsDatabaseMysql()
        )
        app.delete()

    def test_not_found(self):
        try:
            app = DeleteAccount(
                account_id=self.__mock.account_not_found,
                accounts_obj=AccountsOrm(),
                accounts_db_obj=AccountsDatabaseMysql()
            )
            app.delete()

        except NotFound:
            self.assertRaisesMessage(NotFound, 'Account not found')
