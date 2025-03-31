import unittest

from shared.exceptions.invalid_filter import InvalidFilter
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.filter import Filter


class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.filter_values = ["filter_1", "filter_2"]

    def test_can_be_empty(self):
        self.assertEqual(Filter({}, self.filter_values).filters, {})

    def test_must_be_dict(self):
        try:
            Filter(["value_1"], self.filter_values)
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, "Filter has an invalid type.")

    def test_must_be_in_filter_values(self):
        try:
            Filter({"filter_1": "value_1", "filter_invalid": "value"}, self.filter_values)
        except InvalidFilter as ex:
            self.assertEqual(ex.message, "Filter has an invalid value.")

    def test_valid_filter_ok(self):
        self.assertEqual(Filter({"filter_1": "value_1", "filter_2": "value_2"}, self.filter_values).filters,
                         {"filter_1": "value_1", "filter_2": "value_2"})
