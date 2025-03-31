from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class Priority:

    def __init__(self, priority):
        self.__name = 'priority'
        self.priority = priority

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        if not isinstance(priority, str):
            raise TypeErrorValue(self.__name)

        priority = priority.strip()
        if not priority:
            raise InvalidValue(self.__name)

        if priority not in ['low', 'normal', 'medium', 'high', 'urgent']:
            raise InvalidValue(self.__name)

        self.__priority = priority
