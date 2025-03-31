from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.b64 import encode_obj
from src.comments.domain.attachment_desk import AttachmentDesk


class AttachmentsDesk:

    def __init__(self, attachments):
        self.attachments = attachments or []

    @property
    def data(self):
        return [self.__format_attachment(a) for a in self.attachments]

    @property
    def data_encoded(self):
        return encode_obj(self.data)

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        att_ok = []
        for attachment in attachments:
            if not isinstance(attachment, dict):
                raise TypeErrorValue('attachments')

            try:
                att_ok.append(AttachmentDesk(**attachment).data)
            except TypeError:
                raise InvalidValue('attachment')

        self.__attachments = att_ok

    @staticmethod
    def __format_attachment(attachment):
        return {
            'filename': attachment['filename'],
            'type': attachment['type'],
            'filetype': attachment['filetype'],
            'mediatype': attachment['mediatype'],
            'url': attachment['url'],
            'mediasize': attachment['mediasize']
        }
