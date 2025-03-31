from shared.exceptions.generic import GenericException
from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.get_uuid import get_uuid
from shared.infrastructure.timestamps import get_timestamp
from shared.value_objects.author_id import AuthorID
from shared.value_objects.comment import CommentBody
from shared.value_objects.external_id import ExternalID
from shared.value_objects.platform import Platform
from shared.value_objects.priority import Priority
from shared.value_objects.status import Status
from shared.value_objects.subject import Subject
from shared.value_objects.tags import Tags
from shared.value_objects.unique_id import UniqueID


class TicketIn:
    def __init__(self, subject='', description='', requester_id=None, author_id=None, assignee_id=None, status=None,
                 status_id=None, platform=None, channel_id=None, priority=None, priority_id=None, external_id=None,
                 tags=None, centribot_project_id=None, centribot_channel_id=None, ticket_id=None, public=True,
                 description_json=None):
        self.ticket_id = ticket_id or get_uuid()
        self.subject = subject
        self.description = description
        self.description_json = description_json
        self.requester_id = requester_id
        self.author_id = author_id
        self.assignee_id = assignee_id
        self.is_agent = False
        self.status = status
        self.status_id = status_id
        self.channel_id = channel_id
        self.platform = platform
        self.priority = priority
        self.priority_id = priority_id
        self.external_id = external_id
        self.tags = tags
        self.centribot_project_id = centribot_project_id
        self.centribot_channel_id = centribot_channel_id
        self.public = public
        self.timestamp = get_timestamp()

        self.__check()

    @property
    def author_id(self):
        return self.__author_id

    @author_id.setter
    def author_id(self, author_id):
        self.__author_id = AuthorID(author_id).author_id

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
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = Subject(subject).subject

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = CommentBody(description).text

    @property
    def description_json(self):
        return self.__description_json

    @description_json.setter
    def description_json(self, description_json):
        if description_json:
            if not isinstance(description_json, dict):
                raise TypeErrorValue('description json')

        self.__description_json = description_json

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
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        value = None
        if channel_id:
            try:
                channel_id = UniqueID(channel_id)
            except Exception:
                raise TypeErrorValue('channel ID')

            value = channel_id.value

        self.__channel_id = value

    @property
    def platform(self):
        return self.__platform

    @platform.setter
    def platform(self, platform):
        if platform:
            platform = Platform(platform).platform

        self.__platform = platform

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = Priority(priority).priority if priority else 'low'

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

    @property
    def centribot_project_id(self):
        return self.__centribot_project_id

    @centribot_project_id.setter
    def centribot_project_id(self, centribot_project_id):
        value = None
        if centribot_project_id:
            try:
                centribot_project_id = UniqueID(centribot_project_id)
            except Exception:
                raise TypeErrorValue('centribot project ID')

            value = centribot_project_id.value

        self.__centribot_project_id = value

    @property
    def centribot_channel_id(self):
        return self.__centribot_channel_id

    @centribot_channel_id.setter
    def centribot_channel_id(self, centribot_channel_id):
        value = None
        if centribot_channel_id:
            try:
                centribot_channel_id = UniqueID(centribot_channel_id)
            except Exception:
                raise TypeErrorValue('centribot channel ID')

            value = centribot_channel_id.value

        self.__centribot_channel_id = value

    @property
    def public(self):
        return self.__public

    @public.setter
    def public(self, public):
        if not isinstance(public, bool):
            raise TypeErrorValue('public')

        self.__public = public

    def __check(self):
        if not self.platform and not self.channel_id:
            raise GenericException('platform or channel_id is required')

        if (self.centribot_project_id or self.centribot_channel_id) and not \
                (self.centribot_project_id or self.centribot_channel_id or self.external_id):
            raise GenericException('centribot values required')

        if not self.author_id and not self.requester_id:
            raise GenericException('AuthorID or RequesterID is required')
