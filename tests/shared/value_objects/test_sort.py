import unittest

from shared.exceptions.invalid_sort import InvalidSort
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.sort import Sort


class TestSort(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_values = ["value_1", "value_2"]

    def test_can_be_none(self):
        self.assertEqual(Sort(None, self.valid_values).sort, None)

    def test_must_be_str(self):
        try:
            Sort(5, self.valid_values)
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, "Sort has an invalid type.")

    def test_must_be_in_valid_values(self):
        try:
            Sort("value_3", self.valid_values)
        except InvalidSort as ex:
            self.assertEqual(ex.message, "Sort has an invalid value.")

    def test_valid_value_ok(self):
        self.assertEqual(Sort("value_1", self.valid_values).sort, "value_1")
