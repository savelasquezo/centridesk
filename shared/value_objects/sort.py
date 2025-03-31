from shared.exceptions.invalid_sort import InvalidSort
from shared.exceptions.type_error import TypeErrorValue


class Sort:

    def __init__(self, sort, valid_values):
        self.__name = 'sort'
        self.valid_values = valid_values
        self.sort = sort

    @property
    def sort(self):
        return self.__sort

    @sort.setter
    def sort(self, sort):
        if sort and not isinstance(sort, str):
            raise TypeErrorValue(self.__name)

        sort = sort.strip() if sort else None
        if sort and sort not in self.valid_values:
            raise InvalidSort()

        self.__sort = sort
