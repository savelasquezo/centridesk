from django.test import SimpleTestCase

from src.comments.application.get_comments import GetComments
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.comments_mysql import CommentsMysql
from tests.shared.mock.infrastructure.tickets_mysql import TicketsMysql


class TestGetComments(SimpleTestCase):

    def setUp(self) -> None:
        self.__mock = MockData()

    def test_ok(self):
        app = GetComments(
            account_id=self.__mock.account_id1,
            ticket_id=self.__mock.ticket_unique_id1,
            comments_obj=CommentsMysql(),
            tickets_obj=TicketsMysql(),
            sort=self.__mock.sort_created_at,
            order=self.__mock.order_desc,
        )

        expected = [
            {
                'id': 'ca82123116b24267b5f1caaa784af6e4',
                'text': 'Comment 1 text',
                'text_json': None,
                'attachments': [
                    {
                        'type': 'image',
                        'mediatype': 'image/jpg',
                        'url': 'http://url.example.com/s3bucketresource.jpg',
                        'mediasize': '1234'
                    }
                ],
                'author_id': '9177f1af705d46acb4e85afaf3cef30b',
                'is_agent': 0,
                'public': True,
                'ticket_id': '9102302ea0a945bfa6c02439adcdbbef',
                'created_at': '2022-05-25 08:00:00'
            }
        ], 1

        self.assertEqual(app.get(), expected)
