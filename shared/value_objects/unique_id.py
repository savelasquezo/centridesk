from uuid import UUID
from shared.exceptions.type_error import TypeErrorValue


class UniqueID:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise TypeErrorValue('unique ID')

        value = value.strip()
        UUID(value, version=4)

        self.__value = value
