import unittest

from shared.infrastructure.timestamps import from_timestamp_to_date
from src.centribot.infrasctructure.centribot_requests import CentribotRequests
from src.comments.application.create_comment import CommentCreate
from src.comments.application.process_attachments_from_smooch import ProcessAttachmentsSmooch
from src.comments.domain.comment_in import CommentIn
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.agents_mysql import AgentsMysql
from tests.shared.mock.infrastructure.buckets import AwsBuckets
from tests.shared.mock.infrastructure.comments_mysql import CommentsMysql
from tests.shared.mock.infrastructure.comments_websocket import CommentsWebsocket
from tests.shared.mock.infrastructure.customers_mysql import CustomersMysql
from tests.shared.mock.infrastructure.firebase_connector import FirebaseConnector
from tests.shared.mock.infrastructure.get_file_from_url import FileFromUrl
from tests.shared.mock.infrastructure.users_token_orm import UsersTokenOrm


class TestCreateComment(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

        self.returned_ticket1 = {
            'id': self.mock.ticket_unique_id1,
            'auto_id': 1,
            'subject': self.mock.ticket_title,
            'status_id': 2,
            'priority_id': 1,
            'author_id': self.mock.customer_unique_id1,
            'is_agent': False,
            'assignee_id': None,
            'channel_id': self.mock.chat_web_channel_id,
            'centribot_external_id': self.mock.customer_centribot_external_id1,
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
                'name': self.mock.customer_display_name1,
                'email': None,
                'phone': None,
                'centribot_external_id': self.mock.customer_centribot_external_id1,
                'created_at': from_timestamp_to_date(self.mock.created_at),
                'updated_at': None,
                'active': True
            },
            'channel_name': self.mock.channels_dict[self.mock.chat_web_channel_id]
        }

    def test_create_ok_no_attachments(self):
        comment = {
            "text": "Comment text ok",
            "public": True,
            "author_id": self.mock.customer_unique_id1
        }

        comment_in = CommentIn(ticket_id=self.mock.ticket_unique_id1, **comment)

        app = CommentCreate(
            account_id=self.mock.account_id1,
            comment=comment_in,
            ticket=self.returned_ticket1,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm(),
            process_attachments_app=ProcessAttachmentsSmooch()
        )

        expected = {
            'id': comment_in.comment_id,
            'text': comment['text'],
            'text_json': None,
            'attachments': [],
            'author_id': comment['author_id'],
            'is_agent': 0,
            'public': True,
            'ticket_id': self.mock.ticket_unique_id1,
            'created_at': from_timestamp_to_date(comment_in.timestamp)
        }

        self.assertEqual(app.create(), expected)

    def test_create_ok_with_attachments(self):
        comment = {
            "text": "Comment text with attachments",
            "public": True,
            "author_id": self.mock.customer_unique_id1,
            "attachments": [
                {
                    "type": "image",
                    "mediatype": "image/jpg",
                    "url": "https://url.example.com/s3bucketresource.jpg",
                    "mediasize": "1234"
                }
            ]
        }

        comment_in = CommentIn(ticket_id=self.mock.ticket_unique_id1, **comment)

        app = CommentCreate(
            account_id=self.mock.account_id1,
            comment=comment_in,
            ticket=self.returned_ticket1,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm(),
            process_attachments_app=ProcessAttachmentsSmooch()
        )

        expected = {
            'id': comment_in.comment_id,
            'text': "Comment text with attachments",
            'text_json': None,
            'attachments': [
                {
                    "type": "image",
                    "mediatype": "image/jpg",
                    "url": f"https://s3bucketurl.com/centridesk/{self.mock.account_id1}/"
                           f"ticket/{self.mock.ticket_unique_id1}/"
                           f"attachments/{app.process_attachments_app.attachment_id}.jpg",
                    "mediasize": "1234"
                }
            ],
            'author_id': comment['author_id'],
            'is_agent': 0,
            'public': True,
            'ticket_id': self.mock.ticket_unique_id1,
            'created_at': from_timestamp_to_date(comment_in.timestamp)
        }

        self.assertEqual(app.create(), expected)

    def test_create_ok_with_attachments_no_text(self):
        comment = {
            "public": True,
            "author_id": self.mock.customer_unique_id1,
            "attachments": [
                {
                    "type": "image",
                    "mediatype": "image/jpg",
                    "url": "https://url.example.com/s3bucketresource.jpg",
                    "mediasize": "1234"
                }
            ]
        }

        comment_in = CommentIn(ticket_id=self.mock.ticket_unique_id1, **comment)

        app = CommentCreate(
            account_id=self.mock.account_id1,
            comment=comment_in,
            ticket=self.returned_ticket1,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm(),
            process_attachments_app=ProcessAttachmentsSmooch()
        )

        expected = {
            'id': comment_in.comment_id,
            'text': "only_attachment",
            'text_json': None,
            'attachments': [
                {
                    "type": "image",
                    "mediatype": "image/jpg",
                    "url": f"https://s3bucketurl.com/centridesk/{self.mock.account_id1}/"
                           f"ticket/{self.mock.ticket_unique_id1}/"
                           f"attachments/{app.process_attachments_app.attachment_id}.jpg",
                    "mediasize": "1234"
                }
            ],
            'author_id': comment['author_id'],
            'is_agent': 0,
            'public': True,
            'ticket_id': self.mock.ticket_unique_id1,
            'created_at': from_timestamp_to_date(comment_in.timestamp)
        }

        self.assertEqual(app.create(), expected)

    def test_create_ok_private(self):
        comment = {
            "text": "Comment text ok",
            "public": False,
            "author_id": self.mock.customer_unique_id1
        }

        comment_in = CommentIn(ticket_id=self.mock.ticket_unique_id1, **comment)

        app = CommentCreate(
            account_id=self.mock.account_id1,
            comment=comment_in,
            ticket=self.returned_ticket1,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm(),
            process_attachments_app=ProcessAttachmentsSmooch()
        )

        expected = {
            'id': comment_in.comment_id,
            'text': comment['text'],
            'text_json': None,
            'attachments': [],
            'author_id': comment['author_id'],
            'is_agent': 0,
            'public': False,
            'ticket_id': self.mock.ticket_unique_id1,
            'created_at': from_timestamp_to_date(comment_in.timestamp)
        }

        self.assertEqual(app.create(), expected)
