from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.unique_id import UniqueID


class ChannelID:

    def __init__(self, value):
        self.__name = 'channel ID'
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            value = UniqueID(value)
        except Exception:
            raise TypeErrorValue('channel ID')

        self.__value = value
