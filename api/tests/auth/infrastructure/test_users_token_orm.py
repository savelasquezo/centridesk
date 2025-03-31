from django.test import TestCase

from api.tests.shared.database import users_token
from api.tests.shared.mock_data import MockData
from shared.infrastructure.b64 import encode_obj
from src.auth.infrastructure.users_token_orm import UsersTokenOrm


class TestUsersTokenOrm(TestCase):

    @classmethod
    def setUpTestData(cls):
        mock = MockData()

        users_token.create_all(mock)

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_create_ok(self):
        centribot_user_id = '0o8ujk45jki94b069d8582jdu76et5so'

        users_token_obj = UsersTokenOrm(
            centribot_user_id=centribot_user_id,
            created_at=self.__mock.created_at
        )
        result = users_token_obj.create()

        expected = {
            'key': result['key'],
            'centribot_user_id': centribot_user_id,
            'mobile_id': None,
            'created_at': self.__mock.created_at,
            'updated_at': None
        }

        self.assertEqual(result, expected)

    def test_get(self):
        users_token_obj = UsersTokenOrm(centribot_user_id=self.__mock.centribot_user_id1)

        self.assertEqual(users_token_obj.get(), self.__mock.users_token[0])

    def test_get_not_found(self):
        users_token_obj = UsersTokenOrm(centribot_user_id='user_id_not_found')

        self.assertEqual(users_token_obj.get(), None)

    def test_get_by_key(self):
        users_token_obj = UsersTokenOrm(key=self.__mock.token2)

        self.assertEqual(users_token_obj.get_by_key(), self.__mock.users_token[1])

    def test_get_by_key_not_found(self):
        users_token_obj = UsersTokenOrm(key='token_not_found')

        self.assertEqual(users_token_obj.get_by_key(), None)

    def test_update_mobile_id_by_key(self):
        users_token_obj = UsersTokenOrm(
            key=self.__mock.token1,
            mobile_id=encode_obj(['1a2b3c4d5e6f']),
            updated_at=self.__mock.updated_at
        )

        expected = {
            'key': self.__mock.no_expired_user1['key'],
            'centribot_user_id': self.__mock.no_expired_user1['centribot_user_id'],
            'mobile_id': ['1a2b3c4d5e6f'],
            'created_at': self.__mock.no_expired_user1['created_at'],
            'updated_at': self.__mock.updated_at
        }

        self.assertEqual(users_token_obj.update_mobile_id_by_key(), expected)

    def test_update_mobile_id_by_key_with_previous(self):
        users_token_obj = UsersTokenOrm(
            key=self.__mock.token3,
            mobile_id=encode_obj([self.__mock.mobile_id1, '1a2b3c4d5e6f']),
            updated_at=self.__mock.updated_at
        )

        expected = {
            'key': self.__mock.no_expired_user3['key'],
            'centribot_user_id': self.__mock.no_expired_user3['centribot_user_id'],
            'mobile_id': [self.__mock.mobile_id1, '1a2b3c4d5e6f'],
            'created_at': self.__mock.no_expired_user3['created_at'],
            'updated_at': self.__mock.updated_at
        }

        self.assertEqual(users_token_obj.update_mobile_id_by_key(), expected)

    def test_update_mobile_id_by_key_bad_key(self):
        users_token_obj = UsersTokenOrm(
            key='Invalid key',
            mobile_id=encode_obj(['1a2b3c4d5e6f']),
            updated_at=self.__mock.updated_at
        )

        self.assertEqual(users_token_obj.update_mobile_id_by_key(), None)
