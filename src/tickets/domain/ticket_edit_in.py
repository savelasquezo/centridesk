from shared.exceptions.type_error import TypeErrorValue
from shared.exceptions.invalid_value import InvalidValue
from shared.infrastructure.timestamps import get_timestamp
from shared.value_objects.external_id import ExternalID
from shared.value_objects.priority import Priority
from shared.value_objects.status import Status
from shared.value_objects.tags import Tags
from shared.value_objects.unique_id import UniqueID


class TicketEditIn:
    def __init__(self, requester_id=None, assignee_id=None, status=None, status_id=None, priority=None,
                 priority_id=None, external_id=None, tags=None, ticket_id=None):
        self.ticket_id = ticket_id
        self.requester_id = requester_id
        self.assignee_id = assignee_id
        self.is_agent = False
        self.status = status
        self.status_id = status_id
        self.priority = priority
        self.priority_id = priority_id
        self.external_id = external_id
        self.tags = tags
        self.timestamp = get_timestamp()

    @property
    def requester_id(self):
        return self.__requester_id

    @requester_id.setter
    def requester_id(self, requester_id):
        value = None
        if requester_id:
            try:
                requester_id = UniqueID(requester_id)
            except Exception:
                raise TypeErrorValue('requester')
            value = requester_id.value

        self.__requester_id = value

    @property
    def assignee_id(self):
        return self.__assignee_id

    @assignee_id.setter
    def assignee_id(self, assignee_id):
        if assignee_id:
            try:
                assignee_id = UniqueID(assignee_id).value
            except Exception:
                raise TypeErrorValue('agent')

        self.__assignee_id = assignee_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = Status(status).status if status else 'new'

    @property
    def status_id(self):
        return self.__status_id

    @status_id.setter
    def status_id(self, status_id):
        if not isinstance(status_id, int):
            raise TypeErrorValue('status id')

        if status_id not in range(1, 7):
            raise InvalidValue('status id')

        self.__status_id = status_id

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = Priority(priority).priority if priority else 'low'

    @property
    def priority_id(self):
        return self.__priority_id

    @priority_id.setter
    def priority_id(self, priority_id):
        if not isinstance(priority_id, int):
            raise TypeErrorValue('priority id')

        if priority_id not in range(5):
            raise InvalidValue('priority id')

        self.__priority_id = priority_id

    @property
    def external_id(self):
        return self.__external_id

    @external_id.setter
    def external_id(self, external_id):
        if external_id:
            external_id = ExternalID(external_id).external_id

        self.__external_id = external_id

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        if tags:
            tags = Tags(tags).tags

        self.__tags = tags
