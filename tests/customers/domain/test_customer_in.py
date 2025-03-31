from django.test import SimpleTestCase

from shared.infrastructure.b64 import encode_obj
from src.customers.domain.customer_in import CustomerIn


class TestCustomerIn(SimpleTestCase):

    def test_ok(self):
        customer_in = CustomerIn(
            customer_id='c92a905edd7b422b93654e265fb3f895',
            name='Pepe',
            email='pepe@gmail.com',
            phone='+34678678678',
            centribot_external_id='c92a905edd7b422b93654e265fb3f895',
            active=True,
            agent_id='c92a905edd7b422b93654e265fb3f895',
            company='Centribal',
            delegation='Dev',
            external_id='123externalId456',
            gdpr=True
        )

        self.assertEqual(customer_in.customer_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(customer_in.name, 'Pepe')
        self.assertEqual(customer_in.email, 'pepe@gmail.com')
        self.assertEqual(customer_in.phone, '+34678678678')
        self.assertEqual(customer_in.centribot_external_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(customer_in.active, True)
        self.assertEqual(customer_in.agent_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(customer_in.company.encoded, encode_obj('Centribal'))
        self.assertEqual(customer_in.delegation.encoded, encode_obj('Dev'))
        self.assertEqual(customer_in.external_id.encoded, encode_obj('123externalId456'))
        self.assertEqual(customer_in.company.value, 'Centribal')
        self.assertEqual(customer_in.delegation.value, 'Dev')
        self.assertEqual(customer_in.external_id.value, '123externalId456')
        self.assertEqual(customer_in.gdpr, 1)

    def test_ok_only_email(self):
        customer_in = CustomerIn(
            name='Pepe',
            email='pepe@gmail.com',
            gdpr=True
        )

        self.assertIsNotNone(customer_in.customer_id)
        self.assertEqual(customer_in.name, 'Pepe')
        self.assertEqual(customer_in.email, 'pepe@gmail.com')
        self.assertEqual(customer_in.phone, None)
        self.assertEqual(customer_in.external_id.value, None)
        self.assertEqual(customer_in.active, True)
        self.assertEqual(customer_in.agent_id, None)
        self.assertEqual(customer_in.company.value, None)
        self.assertEqual(customer_in.gdpr, 1)

    def test_ok_only_phone(self):
        customer_in = CustomerIn(
            name='Pepe',
            phone='+34678678678',
            gdpr=False
        )

        self.assertIsNotNone(customer_in.customer_id)
        self.assertEqual(customer_in.name, 'Pepe')
        self.assertEqual(customer_in.email, None)
        self.assertEqual(customer_in.phone, '+34678678678')
        self.assertEqual(customer_in.external_id.value, None)
        self.assertEqual(customer_in.active, True)
        self.assertEqual(customer_in.agent_id, None)
        self.assertEqual(customer_in.company.value, None)
        self.assertEqual(customer_in.gdpr, 0)

    def test_ok_only_centribot_external_id(self):
        customer_in = CustomerIn(
            name='Pepe',
            centribot_external_id='c92a905edd7b422b93654e265fb3f895',
            gdpr=True
        )

        self.assertIsNotNone(customer_in.customer_id)
        self.assertEqual(customer_in.name, 'Pepe')
        self.assertEqual(customer_in.email, None)
        self.assertEqual(customer_in.phone, None)
        self.assertEqual(customer_in.centribot_external_id, 'c92a905edd7b422b93654e265fb3f895')
        self.assertEqual(customer_in.active, True)
        self.assertEqual(customer_in.agent_id, None)
        self.assertEqual(customer_in.company.value, None)
        self.assertEqual(customer_in.gdpr, 1)

    def test_without_email_phone_external_id(self):
        try:
            CustomerIn(
                name='Pepe',
                gdpr=True
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Must exist at least one of: email, phone, centribot_external_id")

    def test_invalid_name(self):
        try:
            CustomerIn(
                name=12345,
                centribot_external_id='c92a905edd7b422b93654e265fb3f895'
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Name has an invalid value.")

    def test_invalid_email(self):
        try:
            CustomerIn(
                name='Pepe',
                email=1234
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Email has an invalid type.")

    def test_invalid_company(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                company=12345
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Company has an invalid type.")

    def test_invalid_agent_id(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                agent_id=12345
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Agent id has an invalid type.")

    def test_phone_bad_format(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                phone='687678765'
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Phone has an invalid value.")

    def test_invalid_delegation(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                delegation=12345
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Delegation has an invalid type.")

    def test_empty_delegation(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                delegation=' ',
                gdpr=False
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Delegation is required")

    def test_invalid_external_id(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                external_id=12345
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "External id has an invalid type.")

    def test_empty_external_id(self):
        try:
            CustomerIn(
                name='Pepe',
                email='pepe@gmail.com',
                external_id=' ',
                gdpr=False
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "External id is required")

    def test_invalid_gdpr(self):
        try:
            CustomerIn(
                name='Pepe',
                centribot_external_id='c92a905edd7b422b93654e265fb3f895'
            )
        except Exception as ex:
            self.assertEqual(f"{ex}", "Gdpr has an invalid type.")
