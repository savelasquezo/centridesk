from re import search, sub

from shared.exceptions.invalid_format import InvalidFormat
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class Tag:

    def __init__(self, tag):
        self.__name = 'tag'
        self.tag = tag

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, tag):
        if not isinstance(tag, str):
            raise TypeErrorValue(self.__name)

        tag = tag.strip()
        tag = sub('[^a-zA-Z0-9_]', '', tag)
        if not tag:
            raise InvalidValue(self.__name)

        if not search(r'(^[a-zA-Z0-9_]*$)', tag):
            raise InvalidFormat(self.__name)

        self.__tag = tag.lower()
