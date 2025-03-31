from django.test import TestCase

from src.accounts.infrastructure.accounts_orm import AccountsOrm
from api.tests.shared.database import accounts, token
from api.tests.shared.mock_data import MockData
from shared.exceptions.not_found import NotFound


class TestAccountsOrm(TestCase):

    @classmethod
    def setUpTestData(cls):
        mock = MockData()

        accounts.create_many_by_id(mock, [mock.account_id2])
        token.create(mock.account_id2, 'Centribot')
        token.create(mock.account_id2, 'Testing')

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_create_ok(self):
        db = AccountsOrm(account_id=self.__mock.account_id1, name=self.__mock.account_id1)
        self.assertEqual(db.create(), {'id': self.__mock.account_id1, 'name': self.__mock.account_id1, 'active': True})

    def test_get_ok(self):
        db = AccountsOrm(account_id=self.__mock.account_id2)
        self.assertEqual(db.get(), {'id': self.__mock.account_id2, 'name': self.__mock.account_id2, 'active': True})

    def test_get_not_found(self):
        try:
            db = AccountsOrm(account_id=self.__mock.account_id1)
            db.get()
        except NotFound:
            self.assertRaisesMessage(NotFound, 'Account not found')

    def test_check_exists_true(self):
        db = AccountsOrm(account_id=self.__mock.account_id2)
        self.assertTrue(db.check_exists())

    def test_check_exists_false(self):
        db = AccountsOrm(account_id=self.__mock.account_id1)
        self.assertFalse(db.check_exists())

    def test_delete_ok(self):
        db = AccountsOrm(account_id=self.__mock.account_id2)
        db.delete()

    def test_delete_not_found(self):
        try:
            db = AccountsOrm(account_id=self.__mock.account_id1)
            db.delete()
        except NotFound:
            self.assertRaisesMessage(NotFound, 'Account not found')
