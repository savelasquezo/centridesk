import unittest

from shared.exceptions.invalid_value import InvalidValue
from src.comments.domain.attachments_smooch import AttachmentsSmooch


class TestAttachment(unittest.TestCase):

    def setUp(self):
        self.invalid_attachments = [
            {
                "type": "image",
                "invalid_field": "image/jpg",
                "url": "http://url.example.com/image.jpg",
                "mediasize": "1234"
            }
        ]

        self.invalid_attachments_2 = [
            {
                "type": "image",
                "url": "http://url.example.com/image.jpg",
                "mediasize": "1234"
            }
        ]

        self.valid_attachments = [
            {
                "type": "image",
                "mediatype": "image/jpg",
                "url": "https://url.example.com/image.jpg",
                "mediasize": "1234"
            }
        ]

    def test_default_value_when_none(self):
        self.assertEqual(AttachmentsSmooch(None).attachments, [])

    def test_invalid_fields(self):
        try:
            AttachmentsSmooch(self.invalid_attachments)
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Attachment has an invalid value.')

    def test_need_all_fields(self):
        try:
            AttachmentsSmooch(self.invalid_attachments_2)
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Attachment has an invalid value.')

    def test_all_values_ok(self):
        self.assertEqual(AttachmentsSmooch(self.valid_attachments).attachments, self.valid_attachments)
