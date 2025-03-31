from django.test import SimpleTestCase

from shared.exceptions.invalid_value import InvalidValue
from src.search.domain.search_ticket import SearchTicket


class TestTickets(SimpleTestCase):

    def test_ok_no_query(self):
        tickets = SearchTicket()
        self.assertEqual(tickets.query, None)

    def test_ok_with_query(self):
        tickets = SearchTicket('status_id:1')
        self.assertEqual(tickets.query,
                          [{'type': 'condition', 'field': 'status_id', 'value': '1', 'condition': 'like'}])

    def test_ok_2_queries(self):
        tickets = SearchTicket('status_id:1&&external_id:Test')
        self.assertEqual(tickets.query,
                          [{'type': 'condition', 'field': 'status_id', 'value': '1', 'condition': 'like'},
                           {'type': 'operator', 'operator': '&&'},
                           {'type': 'condition', 'field': 'external_id', 'value': 'Test', 'condition': 'like'}])

    def test_ok_with_generic_query(self):
        tickets = SearchTicket('_:test')
        self.assertEqual(tickets.query, [{'type': 'operator', 'operator': '('},
                                          {'type': 'condition', 'field': 'status_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'priority_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'author_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'assignee_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'channel_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'external_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'centribot_project_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': '||'},
                                          {'type': 'condition', 'field': 'centribot_channel_id', 'value': 'test',
                                           'condition': 'like'}, {'type': 'operator', 'operator': ')'}])

    def test_invalid_filter(self):
        try:
            SearchTicket('----')
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Query has an invalid value.')

    def test_invalid_query_by_field(self):
        try:
            SearchTicket('invalid_field:value1')
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Query (invalid_field) has an invalid value.')
