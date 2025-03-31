import unittest

from shared.exceptions.invalid_filter import InvalidFilter
from shared.exceptions.invalid_sort import InvalidSort
from src.tickets.domain.ticket_filter import TicketFilter


class TestTicketFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_filter = {"created_at": "valid_created_at", "author_id": "valid_author_id"}
        self.invalid_filter = {"created_at": "valid_created_at", "field_not_exist": "invalid_value"}

        self.valid_sort = "created_at"
        self.invalid_sort = "field_not_exist"

        self.valid_order = "desc"

    def test_can_be_only_filters(self):
        ticket_filter = TicketFilter(self.valid_filter, None, None)
        self.assertEqual(ticket_filter.filters, self.valid_filter)
        self.assertEqual(ticket_filter.sort, [])
        self.assertEqual(ticket_filter.order, None)

    def test_can_be_without_order(self):
        ticket_filter = TicketFilter(self.valid_filter, self.valid_sort, None)
        self.assertEqual(ticket_filter.filters, self.valid_filter)
        self.assertEqual(ticket_filter.sort, [self.valid_sort])
        self.assertEqual(ticket_filter.order, [])

    def test_order_without_effect_if_not_sort(self):
        ticket_filter = TicketFilter(self.valid_filter, None, self.valid_order)
        self.assertEqual(ticket_filter.filters, self.valid_filter)
        self.assertEqual(ticket_filter.sort, [])
        self.assertEqual(ticket_filter.order, None)

    def test_all_values_ok(self):
        ticket_filter = TicketFilter(self.valid_filter, self.valid_sort, self.valid_order)
        self.assertEqual(ticket_filter.filters, self.valid_filter)
        self.assertEqual(ticket_filter.sort, [self.valid_sort])
        self.assertEqual(ticket_filter.order, [self.valid_order])

    def test_invalid_ticket_field_in_filter(self):
        try:
            TicketFilter(self.invalid_filter, None, None)
        except InvalidFilter as ex:
            self.assertEqual(ex.message, "Filter has an invalid value.")

    def test_invalid_ticket_field_in_sort(self):
        try:
            TicketFilter(self.valid_filter, self.invalid_sort, None)
        except InvalidSort as ex:
            self.assertEqual(ex.message, "Sort has an invalid value.")
