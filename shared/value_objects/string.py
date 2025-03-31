from shared.exceptions.required_value import RequiredValue
from shared.exceptions.too_long_string import TooLongString
from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.b64 import encode_obj


class String:

    def __init__(self, name, value, required=True, max_characters=None):
        self.__name = name
        self.required = required
        self.max_characters = max_characters
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeErrorValue(self.__name)

            value = value.strip()
            if not value and self.required:
                raise RequiredValue(self.__name)

            if self.max_characters and len(value) > self.max_characters:
                raise TooLongString(self.__name, self.max_characters)

        elif self.required:
            raise RequiredValue(self.__name)

        self.__value = value

    @property
    def encoded(self):
        return encode_obj(self.value)
