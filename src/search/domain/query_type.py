from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class QueryType:

    def __init__(self, query_type):
        self.query_type = query_type

    @property
    def query_type(self):
        return self.__query_type

    @query_type.setter
    def query_type(self, query_type):
        if not isinstance(query_type, str):
            raise TypeErrorValue('search type')

        if query_type not in ['customers', 'tickets']:
            raise InvalidValue('search type')

        self.__query_type = query_type
