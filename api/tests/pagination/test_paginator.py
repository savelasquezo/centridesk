import unittest

from api.shared.pagination.paginator import Paginator
from shared.exceptions.generic import GenericException


class TestPaginator(unittest.TestCase):

    def setUp(self) -> None:
        self.results = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.total = 20
        self.page_size = '5'
        self.page = '2'
        self.element = 'results'
        self.paginator = Paginator(self.page, self.page_size, self.element, self.total, self.results)

    def test_ok(self):
        self.assertEqual(self.paginator.page, int(self.page))
        self.assertEqual(self.paginator.page_size, int(self.page_size))
        self.assertEqual(self.paginator.total, self.total)
        self.assertEqual(self.paginator.element, self.element)
        self.assertEqual(self.paginator.results, self.results)

    def test_invalid_page(self):
        self.page = '0'
        try:
            self.paginator.page = self.page
        except GenericException as ex:
            self.assertEqual(ex.message, 'That page number is less than 1')

    def test_get_response_ok(self):
        expected = {
            self.element: self.results,
            'next_page': 3,
            'previous_page': 1,
            'count': self.total
        }
        self.assertEqual(self.paginator.get_response(), expected)

    def test_get_response_no_page(self):
        self.paginator.page = None
        expected = {
            self.element: self.results,
            'next_page': 2,
            'previous_page': None,
            'count': self.total
        }
        self.assertEqual(self.paginator.get_response(), expected)

    def test_get_response_no_page_size(self):
        self.paginator.page_size = None
        expected = {
            self.element: self.results,
            'next_page': None,
            'previous_page': 1,
            'count': self.total
        }
        self.assertEqual(self.paginator.get_response(), expected)

    def test_get_response_page_max(self):
        self.paginator.page = '40'
        self.paginator.results = []
        expected = {
            self.element: [],
            'next_page': None,
            'previous_page': 4,
            'count': self.total
        }
        self.assertEqual(self.paginator.get_response(), expected)

    def test_get_response_page_first(self):
        self.paginator.page = '1'
        expected = {
            self.element: self.results,
            'next_page': 2,
            'previous_page': None,
            'count': self.total
        }
        self.assertEqual(self.paginator.get_response(), expected)
