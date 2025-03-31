from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.required_value import RequiredValue


class InfoDownloadUsers:

    def __init__(self, info) -> None:
        self.info = info

    @property
    def data(self):
        return {'filter': self.info}

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, value):
        if not value:
            raise RequiredValue('info')

        if not isinstance(value, dict):
            raise InvalidType('info')

        self.__info = value
