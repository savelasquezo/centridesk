import unittest

from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue
from src.comments.domain.comment_in import CommentIn
from tests.shared.mock.data import MockData


class TestCommentIn(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_without_attachments(self):
        comment = {
            "text": "Text",
            "public": True,
            "author_id": self.mock.customer_unique_id1
        }

        comment_in = CommentIn(self.mock.ticket_unique_id1, **comment)

        self.assertEqual(comment_in.text, 'Text')
        self.assertEqual(comment_in.public, True)
        self.assertEqual(comment_in.is_agent, False)
        self.assertEqual(comment_in.author_id, self.mock.customer_unique_id1)
        self.assertEqual(comment_in.attachments.attachments, [])

    def test_with_attachments(self):
        comment = {
            "text": "Text",
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

        comment_in = CommentIn(self.mock.ticket_unique_id1, **comment)

        self.assertEqual(comment_in.text, 'Text')
        self.assertEqual(comment_in.public, True)
        self.assertEqual(comment_in.is_agent, False)
        self.assertEqual(comment_in.author_id, self.mock.customer_unique_id1)
        self.assertEqual(comment_in.attachments.attachments, comment['attachments'])

    def test_text_can_be_empty_with_attachments(self):
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

        comment_in = CommentIn(self.mock.ticket_unique_id1, **comment)

        self.assertEqual(comment_in.text, 'only_attachment')
        self.assertEqual(comment_in.public, True)
        self.assertEqual(comment_in.is_agent, False)
        self.assertEqual(comment_in.author_id, self.mock.customer_unique_id1)
        self.assertEqual(comment_in.attachments.attachments, comment['attachments'])

    def test_text_can_not_be_empty_without_attachments(self):
        try:
            comment = {
                "public": True,
                "author_id": self.mock.customer_unique_id1,
                "attachments": []
            }

            CommentIn(self.mock.ticket_unique_id1, **comment)

        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Text is required')

    def test_ticket_id_must_be_uuid4(self):
        try:
            comment = {
                "text": "Text",
                "public": True,
                "author_id": self.mock.customer_unique_id1,
                "attachments": []
            }

            CommentIn("invalid_ticket_id", **comment)

        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Ticket id has an invalid type.')
