import unittest

from shared.exceptions.invalid_filter import InvalidFilter
from shared.exceptions.invalid_order import InvalidOrder
from shared.exceptions.invalid_sort import InvalidSort
from shared.infrastructure.timestamps import from_timestamp_to_date
from src.tickets.application.tickets_filter import FilterTickets
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.agents_mysql import AgentsMysql
from tests.shared.mock.infrastructure.customers_mysql import CustomersMysql
from tests.shared.mock.infrastructure.tickets_mysql import TicketsMysql


class TestTicketsFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

        self.expected_ticket1 = {
            'id': self.mock.ticket_unique_id1,
            'auto_id': 1,
            'subject': self.mock.ticket_title,
            'status_id': 2,
            'priority_id': 1,
            'author_id': self.mock.customer_unique_id1,
            'is_agent': False,
            'assignee_id': None,
            'channel_id': self.mock.chat_web_channel_id,
            'external_id': self.mock.customer_centribot_external_id1,
            'centribot_project_id': self.mock.centribot_project_id1,
            'centribot_channel_id': self.mock.centribot_channel_id1,
            'tags': self.mock.tags_open,
            'created_at': from_timestamp_to_date(self.mock.created_at),
            'updated_at': None,
            'closed_at': None,
            'status': self.mock.status_dict[2],
            'priority': self.mock.priorities_dict[1],
            'author': {
                'id': self.mock.customer_unique_id1,
                'agent_id': None,
                'name': self.mock.customer_display_name1,
                'email': None,
                'phone': None,
                'centribot_external_id': self.mock.customer_centribot_external_id1,
                'company': None,
                'delegation': None,
                'external_id': None,
                'gdpr': True,
                'gdpr_updated_at': from_timestamp_to_date(self.mock.created_at),
                'last_comment_at': None,
                'created_at': from_timestamp_to_date(self.mock.created_at),
                'updated_at': None,
                'active': True
            },
            'channel_name': self.mock.channels_dict[self.mock.chat_web_channel_id]
        }

        self.expected_ticket2 = {
            'id': self.mock.ticket_unique_id2,
            'auto_id': 2,
            'subject': self.mock.ticket_title,
            'status_id': 2,
            'priority_id': 2,
            'author_id': self.mock.customer_unique_id1,
            'is_agent': False,
            'assignee_id': None,
            'channel_id': self.mock.chat_web_channel_id,
            'external_id': self.mock.customer_centribot_external_id1,
            'centribot_project_id': self.mock.centribot_project_id1,
            'centribot_channel_id': self.mock.centribot_channel_id1,
            'tags': self.mock.tags_open,
            'created_at': from_timestamp_to_date(self.mock.created_at + 10),
            'updated_at': from_timestamp_to_date(self.mock.updated_at),
            'closed_at': None,
            'status': self.mock.status_dict[2],
            'priority': self.mock.priorities_dict[2],
            'author': {
                'id': self.mock.customer_unique_id1,
                'agent_id': None,
                'name': self.mock.customer_display_name1,
                'email': None,
                'phone': None,
                'centribot_external_id': self.mock.customer_centribot_external_id1,
                'company': None,
                'delegation': None,
                'external_id': None,
                'last_comment_at': None,
                'gdpr': True,
                'gdpr_updated_at': from_timestamp_to_date(self.mock.created_at),
                'created_at': from_timestamp_to_date(self.mock.created_at),
                'updated_at': None,
                'active': True
            },
            'channel_name': self.mock.channels_dict[self.mock.chat_web_channel_id]
        }

    def test_invalid_body(self):
        try:
            app = FilterTickets(
                account_id=self.mock.account_id1,
                filters=self.mock.filter_by_invalid_field,
                sort=self.mock.sort_invalid,
                order=self.mock.order_desc,
                tickets_obj=TicketsMysql(),
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql(),
                status_dict=self.mock.status_dict,
                priorities_dict=self.mock.priorities_dict,
                channels_dict=self.mock.channels_dict
            )

            app.get()

        except InvalidFilter as ex:
            self.assertEqual(ex.message, 'Filter has an invalid value.')

    def test_invalid_sort(self):
        try:
            app = FilterTickets(
                account_id=self.mock.account_id1,
                filters=self.mock.filter_by_author_id1_status2,
                sort=self.mock.sort_invalid,
                order=self.mock.order_desc,
                tickets_obj=TicketsMysql(),
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql(),
                status_dict=self.mock.status_dict,
                priorities_dict=self.mock.priorities_dict,
                channels_dict=self.mock.channels_dict
            )

            app.get()

        except InvalidSort as ex:
            self.assertEqual(ex.message, 'Sort has an invalid value.')

    def test_invalid_order(self):
        try:
            app = FilterTickets(
                account_id=self.mock.account_id1,
                filters=self.mock.filter_by_author_id1_status2,
                sort=self.mock.sort_created_at,
                order=self.mock.order_invalid,
                tickets_obj=TicketsMysql(),
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql(),
                status_dict=self.mock.status_dict,
                priorities_dict=self.mock.priorities_dict,
                channels_dict=self.mock.channels_dict
            )

            app.get()

        except InvalidOrder as ex:
            self.assertEqual(ex.message, 'Order has an invalid value.')

    def test_no_params(self):
        app = FilterTickets(
            account_id=self.mock.account_id1,
            filters=self.mock.filter_by_author_id1_status2,
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict=self.mock.status_dict,
            priorities_dict=self.mock.priorities_dict,
            channels_dict=self.mock.channels_dict
        )

        expected = [
            self.expected_ticket1,
            self.expected_ticket2
        ], 2

        self.assertEqual(app.get(), expected)

    def test_params_ok(self):
        app = FilterTickets(
            account_id=self.mock.account_id1,
            filters=self.mock.filter_by_author_id1_status2,
            sort=self.mock.sort_created_at,
            order=self.mock.order_desc,
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict=self.mock.status_dict,
            priorities_dict=self.mock.priorities_dict,
            channels_dict=self.mock.channels_dict
        )

        expected = [
            self.expected_ticket2,
            self.expected_ticket1
        ], 2

        self.assertEqual(app.get(), expected)

    def test_ok_by_status_and_priority(self):
        app = FilterTickets(
            account_id=self.mock.account_id1,
            filters={"status_id": 2, "priority_id": 1},
            sort=self.mock.sort_created_at,
            order=self.mock.order_desc,
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict=self.mock.status_dict,
            priorities_dict=self.mock.priorities_dict,
            channels_dict=self.mock.channels_dict,
            logic_operator='and'
        )

        expected = [
            self.expected_ticket1
        ], 1

        self.assertEqual(app.get(), expected)

    def test_ok_by_status_or_priority(self):
        app = FilterTickets(
            account_id=self.mock.account_id1,
            filters={"status_id": 2, "priority_id": 1},
            sort=self.mock.sort_created_at,
            order=self.mock.order_desc,
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict=self.mock.status_dict,
            priorities_dict=self.mock.priorities_dict,
            channels_dict=self.mock.channels_dict,
            logic_operator='or'
        )

        expected = [
            self.expected_ticket2,
            self.expected_ticket1
        ], 2

        self.assertEqual(app.get(), expected)
