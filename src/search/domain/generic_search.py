import re

from shared.customers.application.format_filter import format_complete_fields, format_condition, format_operator, \
    check_field
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.invalid_value import InvalidValue
from shared.value_objects.order import Order
from shared.value_objects.sort import Sort


class GenericSearch:

    def __init__(self, query=None, fields=None, sort=None, order=None, valid_sort_fields=None):
        self.valid_operators = ['&&', '||', '(', ')']
        self.fields = fields
        self.valid_sort_fields = valid_sort_fields
        self.sort = sort
        self.order = order
        self.query = query

    @property
    def query(self):
        return self.__query

    @query.setter
    def query(self, query):
        if query:
            if not re.fullmatch(r"(\(*[a-z_]+:[\w.@À-ÿ]+[||&&)]*)+", query):
                raise InvalidValue(f'query')

            params = re.split(r"(&&|\|\||[()])", query)
            query = []

            for param in params:
                if param:
                    if param not in self.valid_operators:
                        # Is condition
                        v = param.split(':')
                        field = v[0]
                        value = v[1]

                        if not isinstance(value, str):
                            raise InvalidType(f'Query ({field}) value')

                        if field == '_':
                            query.extend(format_complete_fields(self.fields, value))
                        else:
                            field = check_field(field)
                            if field not in self.fields:
                                raise InvalidValue(f'Query ({field})')

                            query.append(format_condition(field, value))
                    else:
                        # Is operator
                        query.append(format_operator(param))

        self.__query = query

    @property
    def sort(self):
        return self.__sort

    @sort.setter
    def sort(self, sort):
        __sort = sort.split(',') if sort else []

        self.__sort = []
        for s in __sort:
            s = check_field(s.strip())
            self.__sort.append(Sort(s, self.valid_sort_fields).sort)

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        __order = order.split(',') if order else []
        self.__order = [Order(o).order for o in __order] if self.sort else None
