import unittest

from src.users.domain.users_device_edit_in import UsersDeviceEditIn
from shared.exceptions.generic import GenericException


class TestUsersDeviceEditIn(unittest.TestCase):

    def setUp(self) -> None:
        self.mobile_id = 'abcdafdb09874448b4ad7339cffb4151'

    def test_mobile_ok(self):
        user_device = UsersDeviceEditIn(self.mobile_id)
        self.assertEqual(user_device.mobile_id, self.mobile_id)

    def test_invalid_mobile_id(self):
        try:
            UsersDeviceEditIn(True)
        except GenericException as ex:
            self.assertEqual(ex.message, "Mobile id has an invalid value")

    def test_empty_mobile_id(self):
        try:
            UsersDeviceEditIn('  ')
        except GenericException as ex:
            self.assertEqual(ex.message, "Mobile id has an invalid value")
