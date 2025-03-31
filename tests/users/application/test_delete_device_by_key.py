import unittest

from src.users.application.delete_device_by_token import DeleteUserDeviceByKey
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.users_token_orm import UsersTokenOrm


class TestDeleteDevice(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_ok(self):
        delete_device_app = DeleteUserDeviceByKey(
            key=self.mock.user_token_key1,
            mobile_id=self.mock.user_token_mobile_id1,
            userstoken_obj=UsersTokenOrm()
        )

        result = delete_device_app.delete()

        expected = {
            'centribot_user_id': self.mock.user_token_centribot_user_id1,
            'mobile_id': [],
            'created_at': self.mock.created_at,
            'key': self.mock.user_token_key1,
            'updated_at': result['updated_at']
        }

        self.assertEqual(expected, result)
