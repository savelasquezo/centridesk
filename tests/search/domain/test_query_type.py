from django.test import SimpleTestCase

from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue
from src.search.domain.query_type import QueryType
from tests.shared.mock.data import MockData


class TestSearchQuery(SimpleTestCase):
    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok_customers(self):
        search = QueryType('customers')

        self.assertEqual(search.query_type, 'customers')

    def test_ok_tickets(self):
        search = QueryType('tickets')

        self.assertEqual(search.query_type, 'tickets')

    def test_invalid_query_type(self):
        try:
            QueryType(2)
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Search type has an invalid type.')

    def test_invalid_query_option(self):
        try:
            QueryType('test')
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Search type has an invalid value.')
