from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class Platform:

    def __init__(self, platform):
        self.__name = 'platform'
        self.platform = platform

    @property
    def platform(self):
        return self.__platform

    @platform.setter
    def platform(self, platform):
        if not isinstance(platform, str):
            raise TypeErrorValue(self.__name)

        platform = platform.strip()
        if not platform:
            raise InvalidValue(self.__name)

        self.__platform = platform
