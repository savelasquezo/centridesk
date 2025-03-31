from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.b64 import encode_obj
from src.comments.domain.attachment_smooch import AttachmentSmooch


class AttachmentsSmooch:

    def __init__(self, attachments):
        self.attachments = attachments or []

    @property
    def data(self):
        return [a for a in self.attachments]

    @property
    def data_encoded(self):
        return encode_obj(self.data)

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        for attachment in attachments:
            if not isinstance(attachment, dict):
                raise TypeErrorValue('attachments')

            try:
                AttachmentSmooch(**attachment)
            except TypeError:
                raise InvalidValue('attachment')

        self.__attachments = attachments
