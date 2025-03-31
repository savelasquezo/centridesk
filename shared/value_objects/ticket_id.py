from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.unique_id import UniqueID


class TicketID:
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id

    @property
    def ticket_id(self):
        return self.__ticket_id

    @ticket_id.setter
    def ticket_id(self, ticket_id):
        try:
            ticket_id = UniqueID(ticket_id)
        except Exception:
            raise TypeErrorValue('Ticket ID')

        self.__ticket_id = ticket_id.value
