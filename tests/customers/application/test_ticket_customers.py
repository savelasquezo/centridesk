from django.test import SimpleTestCase

from src.customers.application.ticket_customers import TicketCustomers
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.channels_mysql import ChannelsMysql
from tests.shared.mock.infrastructure.status_orm import StatusOrm
from tests.shared.mock.infrastructure.tickets_mysql import TicketsMysql


class TestTicketCustomers(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok_all(self):
        customers = [{
            'id': '6a8db7c42b9ac70208fa14ea7d75c7d11317d462',
            'agent_id': 'b20997c0cfdd4e7fa902ad7b89afd2ff',
            'name': 'Centribot User 3',
            'email': 'customer3@mail.com',
            'phone': '+34678678678',
            'centribot_external_id': '6a8db7c42b9ac70208fa14ea7d75c7d11317d462',
            'company': 'Compañía',
            'delegation': 'Develop',
            'external_id': 'ID-654321',
            'gdpr': True,
            'gdpr_updated_at': '2022-06-01 16:48:27',
            'last_comment_at': None,
            'created_at': '2022-06-01 16:48:27',
            'updated_at': None,
            'active': True
        }]

        app_tc = TicketCustomers(
            account_id=self.__mock.account_id1,
            customers=customers,
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )

        expected = [{
            'id': self.__mock.customer_unique_id3,
            'agent_id': self.__mock.user_id1,
            'name': self.__mock.customer_display_name3,
            'email': self.__mock.customer_email3,
            'phone': self.__mock.customer_phone3,
            'centribot_external_id': self.__mock.customer_centribot_external_id3,
            'company': self.__mock.customer_company,
            'delegation': self.__mock.customer_delegation,
            'last_comment_at': None,
            'external_id': self.__mock.external_id2,
            'gdpr': True,
            'gdpr_updated_at': self.__mock.customer_created_date3,
            'created_at': self.__mock.customer_created_date3,
            'updated_at': None,
            'active': True,
            'last_ticket_status': 'solved',
            'last_ticket_channel': 'Chat Web'
        }]

        self.assertEqual(app_tc.process(), expected)

    def test_ok_no_customers(self):
        app = TicketCustomers(
            account_id=self.__mock.account_id1,
            customers=[],
            tickets_obj=TicketsMysql(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql()
        )

        expected = []

        self.assertEqual(app.process(), expected)
