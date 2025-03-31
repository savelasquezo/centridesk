import unittest

from src.tickets.domain.ticket_create_in import TicketIn
from shared.exceptions.generic import GenericException
from shared.exceptions.invalid_format import InvalidFormat
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class TestTicketIn(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = 'Ticket Subject'
        self.description = 'Ticket Description'
        self.requester_id = '88decffd08eb41538b6837ea4827b02a'
        self.author_id = '7cccbcee3c5c4a42bcb582396f1c9a05'
        self.assignee_id = 'f5a0fe0228634ff5aebdb932cf8b5cdd'
        self.status = 'new'
        self.status_id = '77079470b8d14fe78bec27802f5d32a9'
        self.platform = 'chatweb'
        self.channel_id = 'c8a3c529715f4dbcb092166fe273468b'
        self.priority = 'low'
        self.priority_id = 'fee8b96df0bc4e0db2114c89eaf823c0'
        self.external_id = 'e56bfae1ed52412aacec0d24ed26b044'
        self.tags = ['test1']
        self.centribot_project_id = '30d12dc7764a499d85ac6337d5e40757'
        self.centribot_channel_id = 'ed09744e1b8d42acaea4f5391d64ea98'

    def test_ok(self):
        ticket = TicketIn(
            subject=self.subject,
            description=self.description,
            requester_id=self.requester_id,
            author_id=self.author_id,
            assignee_id=self.assignee_id,
            status=self.status,
            status_id=self.status_id,
            platform=self.platform,
            channel_id=self.channel_id,
            priority=self.priority,
            priority_id=self.priority_id,
            external_id=self.external_id,
            tags=self.tags,
            centribot_project_id=self.centribot_project_id,
            centribot_channel_id=self.centribot_channel_id
        )
        self.assertEqual(ticket.subject, self.subject)
        self.assertEqual(ticket.description, self.description)
        self.assertEqual(ticket.requester_id, self.requester_id)
        self.assertEqual(ticket.author_id, self.author_id)
        self.assertEqual(ticket.assignee_id, self.assignee_id)
        self.assertEqual(ticket.status, self.status)
        self.assertEqual(ticket.status_id, self.status_id)
        self.assertEqual(ticket.platform, self.platform)
        self.assertEqual(ticket.priority, self.priority)
        self.assertEqual(ticket.priority_id, self.priority_id)
        self.assertEqual(ticket.external_id, self.external_id)
        self.assertEqual(ticket.tags, self.tags)
        self.assertEqual(ticket.centribot_project_id, self.centribot_project_id)
        self.assertEqual(ticket.centribot_channel_id, self.centribot_channel_id)

    def test_ok_minimal(self):
        ticket = TicketIn(
            subject=self.subject,
            description=self.description,
            platform=self.platform,
            author_id=self.author_id
        )
        self.assertEqual(ticket.subject, self.subject)
        self.assertEqual(ticket.description, self.description)
        self.assertEqual(ticket.requester_id, None)
        self.assertEqual(ticket.author_id, self.author_id)
        self.assertEqual(ticket.assignee_id, None)
        self.assertEqual(ticket.status, 'new')
        self.assertEqual(ticket.status_id, None)
        self.assertEqual(ticket.platform, self.platform)
        self.assertEqual(ticket.priority, 'low')
        self.assertEqual(ticket.priority_id, None)
        self.assertEqual(ticket.external_id, None)
        self.assertEqual(ticket.tags, None)
        self.assertEqual(ticket.centribot_project_id, None)
        self.assertEqual(ticket.centribot_channel_id, None)

    def test_invalid_author(self):
        try:
            TicketIn(
                author_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Author id has an invalid type.')

    def test_invalid_requester_id(self):
        try:
            TicketIn(
                requester_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Requester has an invalid type.')

    def test_subject_error_type(self):
        try:
            TicketIn(
                subject=1234,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Subject has an invalid type.')

    def test_subject_required(self):
        try:
            TicketIn(
                subject='  ',
                description=self.description,
                platform=self.platform
            )
        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Subject is required')

    def test_description_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=1234,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Text has an invalid type.')

    def test_description_required(self):
        try:
            TicketIn(
                subject=self.subject,
                description='   ',
                platform=self.platform
            )
        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Text is required')

    def test_invalid_assignee_id(self):
        try:
            TicketIn(
                assignee_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Agent has an invalid type.')

    def test_status_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                status=23
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Status has an invalid type.')

    def test_status_invalid_value(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                status='  '
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Status has an invalid value.')

    def test_status_invalid_option(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                status='processed'
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Status has an invalid value.')

    def test_invalid_channel_id(self):
        try:
            TicketIn(
                channel_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Channel id has an invalid type.')

    def test_platform_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=23
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Platform has an invalid type.')

    def test_platform_invalid_value(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform='    '
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Platform has an invalid value.')

    def test_priority_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                priority=23
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Priority has an invalid type.')

    def test_priority_invalid_value(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                priority='  '
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Priority has an invalid value.')

    def test_priority_invalid_option(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                priority='super'
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Priority has an invalid value.')

    def test_external_id_channel_id(self):
        try:
            TicketIn(
                external_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                author_id=self.author_id
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'External id has an invalid type.')

    def test_tags_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                tags=23
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Tags has an invalid type.')

    def test_tag_error_type(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                tags=['123', 23]
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Tag has an invalid type.')

    def test_tag_invalid_value(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                tags=['123', '  ']
            )
        except InvalidValue as ex:
            self.assertEqual(ex.message, 'Tag has an invalid value.')

    def test_tag_invalid_format(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                platform=self.platform,
                tags=['123', 'tag!'],
                author_id=self.author_id
            )
        except InvalidFormat as ex:
            self.assertEqual(ex.message, 'Tag has an invalid format.')

    def test_invalid_centribot_project_id(self):
        try:
            TicketIn(
                centribot_project_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Centribot project id has an invalid type.')

    def test_invalid_centribot_channel_id(self):
        try:
            TicketIn(
                centribot_channel_id='Test',
                subject=self.subject,
                description=self.description,
                platform=self.platform
            )
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, 'Centribot channel id has an invalid type.')

    def test_platform_or_channel_required(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description
            )
        except GenericException as ex:
            self.assertEqual(ex.message, 'platform or channel_id is required')

    def test_centribot_values_required(self):
        try:
            TicketIn(
                subject=self.subject,
                description=self.description,
                requester_id=self.requester_id,
                platform=self.platform,
                centribot_project_id=self.centribot_project_id,
                external_id=None
            )
        except GenericException as ex:
            self.assertEqual(ex.message, 'centribot values required')
