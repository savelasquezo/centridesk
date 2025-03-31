import unittest

from shared.infrastructure.timestamps import from_timestamp_to_date
from src.comments.domain.comment_out import CommentOut
from tests.shared.mock.data import MockData


class TestCommentOut(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_all_values_ok(self):
        expected = {
            'id': self.mock.comment_unique_id1,
            'text': self.mock.comment_text1,
            'text_json': None,
            'attachments': self.mock.comment_attachments1,
            'author_id': self.mock.customer_unique_id1,
            'is_agent': False,
            'public': True,
            'ticket_id': self.mock.ticket_unique_id1,
            'created_at': from_timestamp_to_date(self.mock.created_at)
        }

        self.assertEqual(CommentOut(self.mock.comments[self.mock.account_id1][0]).data, expected)
