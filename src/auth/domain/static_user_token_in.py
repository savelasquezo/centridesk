from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.infrastructure.timestamps import get_timestamp


class StaticUserTokenIn:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.timestamp_at = get_timestamp()

        self.data = {
            'username': self.username,
            'password': self.password
        }

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise InvalidValue('username')

        username = username.strip()
        if not username:
            raise RequiredValue('username')

        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if not isinstance(password, str):
            raise InvalidValue('password')

        password = password.strip()
        if not password:
            raise RequiredValue('password')

        self.__password = password
