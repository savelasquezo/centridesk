import unittest

from src.comments.application.process_attachments_from_smooch import ProcessAttachmentsSmooch
from src.comments.domain.attachments_smooch import AttachmentsSmooch
from tests.shared.mock.data import MockData
from tests.shared.mock.infrastructure.buckets import AwsBuckets
from tests.shared.mock.infrastructure.get_file_from_url import FileFromUrl


class TestProcessAttachments(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_process_ok(self):
        attachments = AttachmentsSmooch([
            {
                "type": "image",
                "mediatype": "image/jpg",
                "url": "https://url.example.com/s3bucketresource.jpg",
                "mediasize": "1234"
            }
        ])

        app = ProcessAttachmentsSmooch(
            account_id=self.mock.account_id1,
            attachments=attachments,
            get_file_obj=FileFromUrl(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            ticket_id=self.mock.ticket_unique_id1
        )

        expected = [
            {
                "type": "image",
                "mediatype": "image/jpg",
                "url": f"https://s3bucketurl.com/centridesk/{self.mock.account_id1}/"
                       f"ticket/{self.mock.ticket_unique_id1}/"
                       f"attachments/{app.attachment_id}.jpg",
                "mediasize": "1234"
            }
        ]

        self.assertEqual(app.process_attachments(), expected)
