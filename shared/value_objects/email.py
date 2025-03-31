from re import search

from shared.exceptions.invalid_format import InvalidFormat
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.required_value import RequiredValue


class Email:
    def __init__(self, email):
        self.__name = 'email'
        self.email = email

    def __repr__(self):
        return self.email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise InvalidType(self.__name)

        email = email.strip()
        if not email:
            raise RequiredValue(self.__name)

        if not search(r'^[\w.-/+]+@(?:[\w-]+[.][\w-]+)+$', email):
            raise InvalidFormat(self.__name)

        self.__email = email
