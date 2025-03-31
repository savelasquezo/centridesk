from django.test import SimpleTestCase

from api.tests.shared.mock_data import MockData
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from src.auth.domain.static_user_token_in import StaticUserTokenIn


class TestStaticUserTokenIn(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        no_expired_validation = StaticUserTokenIn(username=self.__mock.username, password=self.__mock.password)

        expected = {'username': self.__mock.username, 'password': self.__mock.password}

        self.assertEqual(no_expired_validation.data, expected)

    def test_username_invalid_value(self):
        try:
            StaticUserTokenIn(username=33, password=self.__mock.password)

        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Username has an invalid value.')

    def test_username_required(self):
        try:
            StaticUserTokenIn(username=' ', password=self.__mock.password)

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Username is required')

    def test_password_invalid_value(self):
        try:
            StaticUserTokenIn(username=self.__mock.username, password=44)

        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Password has an invalid value.')

    def test_password_required(self):
        try:
            StaticUserTokenIn(username=self.__mock.username, password=' ')

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Password is required')
