import unittest

from shared.exceptions.not_found import NotFound
from shared.infrastructure.timestamps import from_timestamp_to_date
from src.tickets.application.ticket_create import TicketCreate
from src.tickets.domain.ticket_create_in import TicketIn
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.agents_mysql import AgentsMysql
from tests.shared.mock.infrastructure.channels_mysql import ChannelsMysql
from tests.shared.mock.infrastructure.comments_mysql import CommentsMysql
from tests.shared.mock.infrastructure.customers_mysql import CustomersMysql
from tests.shared.mock.infrastructure.firebase_connector import FirebaseConnector
from tests.shared.mock.infrastructure.priorities_orm import PrioritiesOrm
from tests.shared.mock.infrastructure.status_orm import StatusOrm
from tests.shared.mock.infrastructure.tickets_mysql import TicketsMysql
from tests.shared.mock.infrastructure.tickets_websocket import TicketsWebsocket
from tests.shared.mock.infrastructure.users_token_orm import UsersTokenOrm


class TestTicketCreate(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_create_customer_not_exist(self):
        ticket = {
            "external_id": self.mock.customer_centribot_external_id1,
            "subject": "Test ticket",
            "description": "Test ticket",
            "author_id": self.mock.customer_id_not_exist,
            "platform": "telegram",
            "tags": ["tag1", "tag2", "tag3"]
        }

        try:
            app = TicketCreate(
                account_id=self.mock.account_id1,
                ticket=TicketIn(**ticket),
                tickets_obj=TicketsMysql(),
                comments_obj=CommentsMysql(),
                customers_obj=CustomersMysql(),
                priority_obj=PrioritiesOrm(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql(),
                agents_obj=AgentsMysql(),
                websocket_obj=TicketsWebsocket(),
                firebase_obj=FirebaseConnector(),
                userstoken_obj=UsersTokenOrm()
            )
            app.create()

        except Exception as ex:
            self.assertEqual(f"{ex}", "customer not found")

    def test_create_channel_not_found(self):
        ticket = {
            "external_id": self.mock.customer_centribot_external_id1,
            "subject": "Test ticket",
            "description": "Test ticket",
            "author_id": self.mock.customer_unique_id1,
            "channel_id": self.mock.channel_id_not_exist,
            "tags": ["tag1", "tag2", "tag3"]
        }

        try:
            app = TicketCreate(
                account_id=self.mock.account_id1,
                ticket=TicketIn(**ticket),
                tickets_obj=TicketsMysql(),
                comments_obj=CommentsMysql(),
                customers_obj=CustomersMysql(),
                priority_obj=PrioritiesOrm(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql(),
                agents_obj=AgentsMysql(),
                websocket_obj=TicketsWebsocket(),
                firebase_obj=FirebaseConnector(),
                userstoken_obj=UsersTokenOrm()
            )
            app.create()

        except NotFound as ex:
            self.assertEqual(ex.message, "Channel not found")

    def test_create_platform_not_found(self):
        ticket = {
            "external_id": self.mock.customer_centribot_external_id1,
            "subject": "Test ticket",
            "description": "Test ticket",
            "author_id": self.mock.customer_unique_id1,
            "platform": self.mock.channel_platform_not_exist,
            "tags": ["tag1", "tag2", "tag3"]
        }

        try:
            app = TicketCreate(
                account_id=self.mock.account_id1,
                ticket=TicketIn(**ticket),
                tickets_obj=TicketsMysql(),
                comments_obj=CommentsMysql(),
                customers_obj=CustomersMysql(),
                priority_obj=PrioritiesOrm(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql(),
                agents_obj=AgentsMysql(),
                websocket_obj=TicketsWebsocket(),
                firebase_obj=FirebaseConnector(),
                userstoken_obj=UsersTokenOrm()
            )
            app.create()

        except NotFound as ex:
            self.assertEqual(ex.message, "Platform not found")

    def test_create_no_agent_ok(self):
        ticket = {
            "external_id": self.mock.customer_centribot_external_id1,
            "subject": "Test ticket",
            "description": "Test ticket",
            "author_id": self.mock.customer_unique_id1,
            "platform": "telegram",
            "tags": ["tag1", "tag2", "tag3"],
            "centribot_project_id": self.mock.centribot_project_id1
        }

        ticket_in = TicketIn(**ticket)

        app = TicketCreate(
            account_id=self.mock.account_id1,
            ticket=ticket_in,
            tickets_obj=TicketsMysql(),
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            priority_obj=PrioritiesOrm(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql(),
            agents_obj=AgentsMysql(),
            websocket_obj=TicketsWebsocket(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm()
        )

        expected = {
            "id": ticket_in.ticket_id,
            "auto_id": 5,
            "subject": "Test ticket",
            "status_id": 1,
            "priority_id": 1,
            "author_id": self.mock.customer_unique_id1,
            "is_agent": False,
            "assignee_id": None,
            "channel_id": self.mock.telegram_channel_id,
            "external_id": self.mock.customer_centribot_external_id1,
            "centribot_project_id": self.mock.centribot_project_id1,
            "centribot_channel_id": None,
            "tags": [
                "tag1",
                "tag2",
                "tag3"
            ],
            "created_at": from_timestamp_to_date(ticket_in.timestamp),
            "updated_at": None,
            "closed_at": None,
            "author": {
                "id": self.mock.customer_unique_id1,
                "agent_id": None,
                "name": self.mock.customer_display_name1,
                "email": None,
                "phone": None,
                "centribot_external_id": self.mock.customer_centribot_external_id1,
                "company": None,
                "delegation": None,
                'external_id': None,
                'gdpr': True,
                'gdpr_updated_at': from_timestamp_to_date(self.mock.created_at),
                'last_comment_at': None,
                "created_at": from_timestamp_to_date(self.mock.created_at),
                "updated_at": None,
                "active": True
            }
        }

        self.assertEqual(app.create(), expected)

    def test_create_auto_agent_ok(self):
        ticket = {
            "external_id": self.mock.customer_centribot_external_id2,
            "subject": "Test ticket",
            "description": "Test ticket",
            "author_id": self.mock.customer_unique_id2,
            "platform": "telegram",
            "tags": ["tag1", "tag2", "tag3"],
            "centribot_project_id": self.mock.centribot_project_id1
        }

        ticket_in = TicketIn(**ticket)

        app = TicketCreate(
            account_id=self.mock.account_id1,
            ticket=ticket_in,
            tickets_obj=TicketsMysql(),
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            priority_obj=PrioritiesOrm(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql(),
            agents_obj=AgentsMysql(),
            websocket_obj=TicketsWebsocket(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm()
        )

        expected = {
            "id": ticket_in.ticket_id,
            "auto_id": 5,
            "subject": "Test ticket",
            "status_id": 1,
            "priority_id": 1,
            "author_id": self.mock.customer_unique_id2,
            "is_agent": False,
            "assignee_id": self.mock.agent_unique_id1,
            "channel_id": self.mock.telegram_channel_id,
            "external_id": self.mock.customer_centribot_external_id2,
            "centribot_project_id": self.mock.centribot_project_id1,
            "centribot_channel_id": None,
            "tags": [
                "tag1",
                "tag2",
                "tag3"
            ],
            "created_at": from_timestamp_to_date(ticket_in.timestamp),
            "updated_at": None,
            "closed_at": None,
            "author": {
                "id": self.mock.customer_unique_id2,
                "agent_id": self.mock.agent_unique_id1,
                "name": self.mock.customer_display_name2,
                "email": self.mock.customer_email2,
                "phone": self.mock.customer_phone2,
                "centribot_external_id": self.mock.customer_centribot_external_id2,
                "company": self.mock.customer_company,
                "delegation": None,
                'external_id': self.mock.external_id,
                'gdpr': False,
                'gdpr_updated_at': self.mock.customer_created_date2,
                'last_comment_at': None,
                "created_at": self.mock.customer_created_date2,
                "updated_at": None,
                "active": True
            }
        }

        self.assertEqual(app.create(), expected)

    def test_create_ok_status_solved(self):
        ticket = TicketIn(
            subject='New ticket created',
            description='New ticket description',
            platform='chatweb',
            tags=['tag3', 'tag4'],
            author_id=self.mock.customer_unique_id1,
            status='solved'
        )

        app = TicketCreate(
            account_id=self.mock.account_id1,
            ticket=ticket,
            tickets_obj=TicketsMysql(),
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            priority_obj=PrioritiesOrm(),
            status_obj=StatusOrm(),
            channels_obj=ChannelsMysql(),
            agents_obj=AgentsMysql(),
            websocket_obj=TicketsWebsocket(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm()
        )

        output = app.create()

        expected = {
            'id': output['id'],
            'auto_id': len(self.mock.tickets[self.mock.account_id1]) + 1,
            'subject': ticket.subject,
            'status_id': 5,
            'priority_id': 1,
            'author_id': self.mock.customer_unique_id1,
            'is_agent': False,
            'assignee_id': None,
            'channel_id': self.mock.chat_web_channel_id,
            'external_id': ticket.external_id,
            'centribot_project_id': None,
            'centribot_channel_id': None,
            'tags': ticket.tags,
            'created_at': output['created_at'],
            'updated_at': None,
            'closed_at': None,
            'author': {
                'id': self.mock.customer_unique_id1,
                'agent_id': self.mock.customers[self.mock.account_id1][0]['agent_id'],
                'name': self.mock.customer_display_name1,
                'email': self.mock.customers[self.mock.account_id1][0]['email'],
                'phone': self.mock.customers[self.mock.account_id1][0]['phone'],
                'centribot_external_id': self.mock.customer_centribot_external_id1,
                'company': self.mock.customers[self.mock.account_id1][0]['company'],
                'delegation': self.mock.customers[self.mock.account_id1][0]['delegation'],
                'external_id': self.mock.customers[self.mock.account_id1][0]['external_id'],
                'gdpr': self.mock.customers[self.mock.account_id1][0]['gdpr'],
                'gdpr_updated_at': from_timestamp_to_date(self.mock.created_at),
                'last_comment_at': self.mock.customers[self.mock.account_id1][0]['last_comment_at'],
                'created_at': from_timestamp_to_date(self.mock.created_at),
                'updated_at': None,
                'active': True
            }
        }

        self.assertEqual(output, expected)

    def test_create_assignee_not_found(self):
        ticket_in = TicketIn(
            subject='New ticket created',
            description='New ticket description',
            platform='chatweb',
            tags=['tag3', 'tag4'],
            author_id=self.mock.customer_unique_id1,
            status='solved',
            assignee_id='b4246e2edf0e4037a89d5be304e02f3a'
        )

        try:
            app = TicketCreate(
                account_id=self.mock.account_id1,
                ticket=ticket_in,
                tickets_obj=TicketsMysql(),
                comments_obj=CommentsMysql(),
                customers_obj=CustomersMysql(),
                priority_obj=PrioritiesOrm(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql(),
                agents_obj=AgentsMysql(),
                websocket_obj=TicketsWebsocket(),
                firebase_obj=FirebaseConnector(),
                userstoken_obj=UsersTokenOrm()
            )
            app.create()

        except NotFound as ex:
            self.assertEqual(ex.message, "Assignee not found")

    def test_create_assignee_is_trainer(self):
        ticket_in = TicketIn(
            subject='New ticket created',
            description='New ticket description',
            platform='chatweb',
            tags=['tag3', 'tag4'],
            author_id=self.mock.customer_unique_id1,
            status='solved',
            assignee_id=self.mock.role_trainer_id
        )

        try:
            app = TicketCreate(
                account_id=self.mock.account_id1,
                ticket=ticket_in,
                tickets_obj=TicketsMysql(),
                comments_obj=CommentsMysql(),
                customers_obj=CustomersMysql(),
                priority_obj=PrioritiesOrm(),
                status_obj=StatusOrm(),
                channels_obj=ChannelsMysql(),
                agents_obj=AgentsMysql(),
                websocket_obj=TicketsWebsocket(),
                firebase_obj=FirebaseConnector(),
                userstoken_obj=UsersTokenOrm()
            )
            app.create()

        except NotFound as ex:
            self.assertEqual(ex.message, "Assignee not found")
