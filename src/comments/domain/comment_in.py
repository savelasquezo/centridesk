from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.timestamps import get_timestamp
from shared.infrastructure.get_uuid import get_uuid
from src.comments.domain.attachments_smooch import AttachmentsSmooch
from shared.value_objects.author_id import AuthorID
from shared.value_objects.comment import CommentBody
from shared.value_objects.ticket_id import TicketID


class CommentIn:

    def __init__(self, ticket_id, text=None, author_id=None, public=True, is_agent=False, attachments=None,
                 text_json=None):
        self.ticket_id = ticket_id
        self.author_id = author_id
        self.is_agent = is_agent
        self.public = public
        self.attachments = attachments or []
        self.text = text
        self.text_json = text_json
        self.comment_id = get_uuid()
        self.timestamp = get_timestamp()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = CommentBody('only_attachment' if not text and self.attachments else text).text

    @property
    def text_json(self):
        return self.__text_json

    @text_json.setter
    def text_json(self, text_json):
        self.__text_json = text_json

    @property
    def ticket_id(self):
        return self.__ticket_id

    @ticket_id.setter
    def ticket_id(self, ticket_id):
        self.__ticket_id = TicketID(ticket_id).ticket_id

    @property
    def author_id(self):
        return self.__author_id

    @author_id.setter
    def author_id(self, author_id):
        self.__author_id = AuthorID(author_id).author_id

    @property
    def public(self):
        return self.__public

    @public.setter
    def public(self, public):
        if not isinstance(public, bool):
            raise TypeErrorValue('public')

        self.__public = public

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        self.__attachments = AttachmentsSmooch(attachments)
