from django.test import SimpleTestCase

from shared.exceptions.invalid_filter import InvalidFilter
from shared.infrastructure.timestamps import from_timestamp_to_date
from src.customers.application.filter_customers import FilterCustomers
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.channels_mysql import ChannelsMysql
from tests.shared.mock.infrastructure.customers_mysql import CustomersMysql
from tests.shared.mock.infrastructure.status_orm import StatusOrm
from tests.shared.mock.infrastructure.tickets_mysql import TicketsMysql


class TestFilterCustomers(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

        self.expected_customer1 = {
            'id': self.__mock.customer_unique_id1,
            'agent_id': None,
            'name': self.__mock.customer_display_name1,
            'email': None,
            'phone': None,
            'centribot_external_id': self.__mock.customer_centribot_external_id1,
            'company': None,
            'delegation': None,
            'external_id': None,
            'gdpr': True,
            'gdpr_updated_at': from_timestamp_to_date(self.__mock.created_at),
            'last_comment_at': None,
            'created_at': from_timestamp_to_date(self.__mock.created_at),
            'updated_at': None,
            'active': True,
            'last_ticket_status': 'solved',
            'last_ticket_channel': 'Chat Web'
        }

        self.expected_customer2 = {
            'id': self.__mock.customer_unique_id2,
            'agent_id': self.__mock.agent_unique_id1,
            'name': self.__mock.customer_display_name2,
            'email': self.__mock.customer_email2,
            'phone': self.__mock.customer_phone2,
            'centribot_external_id': self.__mock.customer_centribot_external_id2,
            'company': self.__mock.customer_company,
            'delegation': None,
            'external_id': self.__mock.external_id,
            'gdpr': False,
            'gdpr_updated_at': from_timestamp_to_date(self.__mock.customer_created_at2),
            'last_comment_at': None,
            'created_at': from_timestamp_to_date(self.__mock.customer_created_at2),
            'updated_at': None,
            'active': True,
            'last_ticket_channel': None,
            'last_ticket_status': None
        }

        self.expected_customer3 = {
            'id': self.__mock.customer_unique_id3,
            'agent_id': self.__mock.agent_unique_id1,
            'name': self.__mock.customer_display_name3,
            'email': self.__mock.customer_email3,
            'phone': self.__mock.customer_phone3,
            'centribot_external_id': self.__mock.customer_centribot_external_id3,
            'company': self.__mock.customer_company,
            'delegation': self.__mock.customer_delegation,
            'external_id': self.__mock.external_id2,
            'gdpr': True,
            'gdpr_updated_at': from_timestamp_to_date(self.__mock.customer_created_at3),
            'last_comment_at': None,
            'created_at': from_timestamp_to_date(self.__mock.customer_created_at3),
            'updated_at': None,
            'active': True,
            'last_ticket_status': 'solved',
            'last_ticket_channel': 'Chat Web'
        }

    def test_ok_all(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={
                'phone': self.__mock.customer_phone3,
                'email': self.__mock.customer_email3,
                'centribot_external_id': self.__mock.customer_centribot_external_id3,
                'display_name': self.__mock.customer_display_name3,
                'company': 'Compañía'
            },
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )

        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_no_filter(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer1, self.expected_customer2, self.expected_customer3], 3

        self.assertEqual(app.get(), expected)

    def test_sort_order(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={},
            sort=self.__mock.sort_created_at,
            order=self.__mock.order_desc,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer2, self.expected_customer3, self.expected_customer1], 3

        self.assertEqual(app.get(), expected)

    def test_by_phone(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'phone': self.__mock.customer_phone3},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_email(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'email': self.__mock.customer_email3},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_centribot_external_id(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'centribot_external_id': self.__mock.customer_centribot_external_id3},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_name(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'name': self.__mock.customer_display_name3},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_company(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'company': 'Compañía'},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer2, self.expected_customer3], 2

        self.assertEqual(app.get(), expected)

    def test_by_delegation(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'delegation': 'Develop'},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_external_id(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'external_id': 'ID-123456'},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer2], 1

        self.assertEqual(app.get(), expected)

    def test_by_gdpr_true(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'gdpr': True},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer1, self.expected_customer3], 2

        self.assertEqual(app.get(), expected)

    def test_by_gdpr_false(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'gdpr': False},
            sort=None,
            order=None,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer2], 1

        self.assertEqual(app.get(), expected)

    def test_invalid_body(self):
        try:
            app = FilterCustomers(
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                filters=self.__mock.filter_by_invalid_field,
                sort=self.__mock.sort_created_at,
                order=self.__mock.order_desc,
                tickets_obj=TicketsMysql(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql()
            )

            app.get()

        except InvalidFilter as ex:
            self.assertEqual(ex.message, 'Filter has an invalid value.')

    def test_by_company_and_email(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'company': 'Compañía', 'email': self.__mock.customer_email3},
            sort=None,
            order=None,
            logic_operator='and',
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer3], 1

        self.assertEqual(app.get(), expected)

    def test_by_company_or_external_id(self):
        app = FilterCustomers(
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            filters={'company': 'Compañía', 'centribot_external_id': self.__mock.customer_centribot_external_id1},
            sort=None,
            order=None,
            logic_operator='or',
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )
        expected = [self.expected_customer1, self.expected_customer2, self.expected_customer3], 3

        self.assertEqual(app.get(), expected)
