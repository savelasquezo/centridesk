from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class Status:

    def __init__(self, status):
        self.__name = 'status'
        self.status = status

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if not isinstance(status, str):
            raise TypeErrorValue(self.__name)

        status = status.strip()
        if not status:
            raise InvalidValue(self.__name)

        if status not in ['new', 'open', 'pending', 'hold', 'solved', 'closed']:
            raise InvalidValue(self.__name)

        self.__status = status
