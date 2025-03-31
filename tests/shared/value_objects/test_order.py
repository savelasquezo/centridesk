import unittest

from shared.exceptions.invalid_order import InvalidOrder
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.order import Order


class TestOrder(unittest.TestCase):
    def test_must_be_str(self):
        try:
            Order(5)
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, "Order has an invalid type.")

    def test_must_be_in_valid_values(self):
        try:
            Order("invalid_value")
        except InvalidOrder as ex:
            self.assertEqual(ex.message, "Order has an invalid value.")

    def test_valid_order_ok(self):
        self.assertEqual(Order("desc").order, "desc")
