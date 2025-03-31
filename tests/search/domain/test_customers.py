from django.test import SimpleTestCase

from shared.exceptions.invalid_value import InvalidValue
from src.search.domain.search_customer import SearchCustomer


class TestCustomers(SimpleTestCase):

    def test_ok_no_query(self):
        customers = SearchCustomer()
        self.assertEqual(customers.query, None)

    def test_ok_with_query(self):
        customers = SearchCustomer('email:test')
        self.assertEqual(customers.query,
                          [{'type': 'condition', 'field': 'email', 'value': 'test', 'condition': 'like'}])

    def test_ok_2_queries(self):
        customers = SearchCustomer('email:test&&phone:12')
        self.assertEqual(customers.query,
                          [{'type': 'condition', 'field': 'email', 'value': 'test', 'condition': 'like'},
                           {'type': 'operator', 'operator': '&&'},
                           {'type': 'condition', 'field': 'phone', 'value': '12', 'condition': 'like'}])

    def test_ok_with_generic_query(self):
        customers = SearchCustomer('_:test')
        self.assertEqual(customers.query, [{'type': 'operator', 'operator': '('},
                                            {'type': 'condition', 'field': 'phone', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'email', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'centribot_external_id', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'display_name', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'company', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'agent_id', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'delegation', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                            {'type': 'condition', 'field': 'external_id', 'value': 'test',
                                             'condition': 'like'}, {'type': 'operator', 'operator': ')'}])

    def test_invalid_query(self):
        try:
            SearchCustomer('----')
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Query has an invalid value.')

    def test_invalid_query_by_field(self):
        try:
            SearchCustomer('invalid_field:value1')
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Query (invalid_field) has an invalid value.')
