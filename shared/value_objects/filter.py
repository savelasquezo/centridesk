from shared.exceptions.invalid_filter import InvalidFilter
from shared.exceptions.type_error import TypeErrorValue


class Filter:

    def __init__(self, filters, valid_values):
        self.__name = 'filter'
        self.valid_values = valid_values
        self.filters = filters

    @property
    def filters(self):
        return self.__filters

    @filters.setter
    def filters(self, filters):
        if not isinstance(filters, dict):
            raise TypeErrorValue(self.__name)

        for f in filters.keys():
            f = f.strip()
            if f not in self.valid_values:
                raise InvalidFilter()

        self.__filters = filters
