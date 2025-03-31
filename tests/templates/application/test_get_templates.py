import unittest

from shared.exceptions.not_found import NotFound
from src.templates.application.get_templates import GetTemplates
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.accounts_platform_products_orm import AccountsPlatformProductsOrm
from tests.shared.mock.infrastructure.projects_orm import ProjectsOrm
from tests.shared.mock.infrastructure.templates_orm import TemplatesOrm
from tests.shared.mock.infrastructure.webhooks_orm import WebhooksOrm


class TestGetTemplates(unittest.TestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_account_not_exist(self):
        try:
            app = GetTemplates(
                account_id=self.__mock.account_id_not_exist,
                project_id=None,
                accounts_platform_products_orm=AccountsPlatformProductsOrm(),
                projects_orm=ProjectsOrm(),
                templates_orm=TemplatesOrm(),
                webhooks_orm=WebhooksOrm()
            )
            app.get_templates()
        except NotFound as ex:
            self.assertEqual(ex.message, 'Account not found')

    def test_account_have_not_platform_products(self):
        app = GetTemplates(
            account_id=self.__mock.account_id3,
            project_id=None,
            accounts_platform_products_orm=AccountsPlatformProductsOrm(),
            projects_orm=ProjectsOrm(),
            templates_orm=TemplatesOrm(),
            webhooks_orm=WebhooksOrm()
        )

        expected = {
            'campaigns': False,
            'token': None,
            'templates': []
        }

        self.assertEqual(app.get_templates(), expected)

    def test_account_have_not_centripush(self):
        app = GetTemplates(
            account_id=self.__mock.account_id2,
            project_id=None,
            accounts_platform_products_orm=AccountsPlatformProductsOrm(),
            projects_orm=ProjectsOrm(),
            templates_orm=TemplatesOrm(),
            webhooks_orm=WebhooksOrm()
        )

        expected = {
            'campaigns': False,
            'token': None,
            'templates': []
        }

        self.assertEqual(app.get_templates(), expected)

    def test_project_id_does_not_below_to_account(self):
        try:
            app = GetTemplates(
                account_id=self.__mock.account_id1,
                project_id=self.__mock.project_unique_id3,
                accounts_platform_products_orm=AccountsPlatformProductsOrm(),
                projects_orm=ProjectsOrm(),
                templates_orm=TemplatesOrm(),
                webhooks_orm=WebhooksOrm()
            )
            app.get_templates()
        except NotFound as ex:
            self.assertEqual(ex.message, "Project not found")

    def test_get_by_account(self):
        app = GetTemplates(
            account_id=self.__mock.account_id1,
            project_id=None,
            accounts_platform_products_orm=AccountsPlatformProductsOrm(),
            projects_orm=ProjectsOrm(),
            templates_orm=TemplatesOrm(),
            webhooks_orm=WebhooksOrm()
        )

        expected = {
            'campaigns': True,
            'token': self.__mock.webhook_token1,
            'templates': [
                {
                    'id': self.__mock.template_unique_id1,
                    'project_id': self.__mock.template_project_id1,
                    'category': self.__mock.template_category_account_update,
                    'name': self.__mock.template_name1,
                    'language': self.__mock.template_language_es,
                    'header': self.__mock.template_header1,
                    'body': self.__mock.template_body1,
                    'footer': self.__mock.template_footer1,
                    'buttons': self.__mock.template_buttons1,
                    'parameters_count': 0,
                    'status': self.__mock.template_status_approved,
                    'created_at': self.__mock.created_at
                },
                {
                    'id': self.__mock.template_unique_id3,
                    'project_id': self.__mock.template_project_id3,
                    'category': self.__mock.template_category_account_update,
                    'name': self.__mock.template_name3,
                    'language': self.__mock.template_language_es,
                    'header': self.__mock.template_header3,
                    'body': self.__mock.template_body3,
                    'footer': self.__mock.template_footer3,
                    'buttons': self.__mock.template_buttons3,
                    'parameters_count': 0,
                    'status': self.__mock.template_status_approved,
                    'created_at': self.__mock.created_at
                }
            ]
        }

        self.assertEqual(app.get_templates(), expected)

    def test_get_by_project(self):
        app = GetTemplates(
            account_id=self.__mock.account_id1,
            project_id=self.__mock.project_unique_id1,
            accounts_platform_products_orm=AccountsPlatformProductsOrm(),
            projects_orm=ProjectsOrm(),
            templates_orm=TemplatesOrm(),
            webhooks_orm=WebhooksOrm()
        )

        expected = {
            'campaigns': True,
            'token': self.__mock.webhook_token1,
            'templates': [
                {
                    'id': self.__mock.template_unique_id1,
                    'project_id': self.__mock.template_project_id1,
                    'category': self.__mock.template_category_account_update,
                    'name': self.__mock.template_name1,
                    'language': self.__mock.template_language_es,
                    'header': self.__mock.template_header1,
                    'body': self.__mock.template_body1,
                    'footer': self.__mock.template_footer1,
                    'buttons': self.__mock.template_buttons1,
                    'parameters_count': 0,
                    'status': self.__mock.template_status_approved,
                    'created_at': self.__mock.created_at
                }
            ]
        }

        self.assertEqual(app.get_templates(), expected)
