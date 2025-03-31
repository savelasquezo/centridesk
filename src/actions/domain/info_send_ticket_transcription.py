from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.unique_id import UniqueID


class InfoTicketSendTranscription:

    def __init__(self, ticket_id, subject) -> None:
        self.ticket_id = ticket_id
        self.subject = subject

    @property
    def data(self):
        return {
            'ticket_id': self.ticket_id,
            'subject': self.subject
        }

    @property
    def ticket_id(self):
        return self.__ticket_id

    @ticket_id.setter
    def ticket_id(self, value):
        if not isinstance(value, str):
            raise TypeErrorValue('ticket ID')

        value = value.strip()
        if not value:
            raise RequiredValue('ticket ID')

        try:
            value = UniqueID(value)
        except Exception:
            raise TypeErrorValue('ticket ID')

        self.__ticket_id = value.value

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, value):
        if not isinstance(value, str):
            raise TypeErrorValue('subject')

        value = value.strip()
        if not value:
            raise RequiredValue('subject')

        self.__subject = value
