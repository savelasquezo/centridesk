from django.test import SimpleTestCase

from shared.exceptions.generic import GenericException
from shared.exceptions.in_use import InUse
from src.customers.application.create_customer import CreateCustomer
from src.customers.domain.customer_in import CustomerIn
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.agents_mysql import AgentsMysql
from tests.shared.mock.infrastructure.customers_mysql import CustomersMysql


class TestCreateCustomer(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        customer = CustomerIn(
            name=self.__mock.customer_display_name1,
            email=self.__mock.email_not_exist,
            phone=self.__mock.phone_not_exist,
            centribot_external_id=self.__mock.centribot_external_id_not_exist,
            active=True,
            agent_id=self.__mock.user_id1,
            company='Centribal',
            delegation='Dev',
            external_id='ID-000000',
            gdpr=True
        )

        app = CreateCustomer(
            customer=customer,
            account_id=self.__mock.account_id1,
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql()
        )

        expected = {
            'id': customer.customer_id,
            'agent_id': self.__mock.user_id1,
            'name': self.__mock.customer_display_name1,
            'email': self.__mock.email_not_exist,
            'phone': self.__mock.phone_not_exist,
            'centribot_external_id': self.__mock.centribot_external_id_not_exist,
            'company': 'Centribal',
            'delegation': 'Dev',
            'last_comment_at': None,
            'external_id': 'ID-000000',
            'gdpr': 1,
            'gdpr_updated_at': self.__mock.customer_created_date3,
            'created_at': self.__mock.customer_created_date3,
            'updated_at': None,
            'active': True
        }

        self.assertEqual(app.create(), expected)

    def test_repeated_phone(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name1,
                email=self.__mock.email_not_exist,
                phone=self.__mock.customer_phone3,
                centribot_external_id=self.__mock.centribot_external_id_not_exist,
                active=True,
                agent_id=self.__mock.user_id1,
                company='Centribal',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )
            result = app.create()
        except InUse as e:
            result = str(e)

        self.assertEqual(result, 'Phone is in use')

    def test_repeated_email(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name1,
                email=self.__mock.customer_email3,
                phone=self.__mock.phone_not_exist,
                centribot_external_id=self.__mock.centribot_external_id_not_exist,
                active=True,
                agent_id=self.__mock.user_id1,
                company='Centribal',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )
            result = app.create()
        except InUse as e:
            result = str(e)

        self.assertEqual(result, 'Email is in use')

    def test_repeated_centribot_external_id(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name1,
                email=self.__mock.email_not_exist,
                phone=self.__mock.phone_not_exist,
                centribot_external_id=self.__mock.customer_centribot_external_id3,
                active=True,
                agent_id=self.__mock.user_id1,
                company='Centribal',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )
            result = app.create()

        except InUse as e:
            result = str(e)

        self.assertEqual(result, 'Centribot external id is in use')

    def test_agent_not_in_account(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name3,
                email=self.__mock.email_not_exist,
                phone=self.__mock.phone_not_exist,
                centribot_external_id=self.__mock.centribot_external_id_not_exist,
                active=True,
                agent_id=self.__mock.user_id2,
                company='Centribal',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )
            result = app.create()
        except GenericException as e:
            result = str(e)

        self.assertEqual(result, 'Agent not in account')

    def test_user_without_role(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name3,
                email=self.__mock.email_not_exist,
                phone=self.__mock.phone_not_exist,
                centribot_external_id=self.__mock.centribot_external_id_not_exist,
                active=True,
                agent_id=self.__mock.user_id3,
                company='Centribal',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )

            result = app.create()
        except GenericException as e:
            result = str(e)

        self.assertEqual(result, 'Agent role not valid')

    def test_user_role_not_desk(self):
        try:
            customer = CustomerIn(
                name=self.__mock.customer_display_name3,
                email=self.__mock.email_not_exist,
                phone=self.__mock.phone_not_exist,
                centribot_external_id=self.__mock.centribot_external_id_not_exist,
                active=True,
                agent_id=self.__mock.user_id4,
                company='Centribal',
                delegation='Dev',
                external_id='ID-000000',
                gdpr=True
            )

            app = CreateCustomer(
                customer=customer,
                account_id=self.__mock.account_id1,
                customers_obj=CustomersMysql(),
                agents_obj=AgentsMysql()
            )

            result = app.create()
        except GenericException as e:
            result = str(e)

        self.assertEqual(result, 'Agent role not valid')
