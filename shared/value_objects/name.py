from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue


class Name:
    def __init__(self, name):
        self.__str = 'name'
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise InvalidValue(self.__str)

        name = name.strip()
        if not name:
            raise RequiredValue(self.__str)

        self.__name = name
