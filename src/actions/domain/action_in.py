from src.actions.domain.info_download_use_report import InfoDownloadUseReport
from src.actions.domain.info_download_users import InfoDownloadUsers
from src.actions.domain.info_send_ticket_transcription import InfoTicketSendTranscription
from shared.exceptions.empty_object import EmptyObject
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.infrastructure.b64 import encode_obj
from shared.infrastructure.get_uuid import get_uuid
from shared.infrastructure.timestamps import get_timestamp


class Action:
    def __init__(self, action, account_id, requester_id, info=None):
        self.action = action
        self.account_id = account_id
        self.requester_id = requester_id
        self.info = info

        self.unique_id = get_uuid()
        self.created_at = get_timestamp()
        self.result = 0
        self.pending = True
        self.in_progress = False

    @property
    def data(self):
        return {
            'unique_id': self.unique_id,
            'action': self.__action,
            'account_id': self.__account_id,
            'requester_id': self.__requester_id,
            'info': self.__info,
            'result': self.result,
            'pending': self.pending,
            'in_progress': self.in_progress,
            'created_at': self.created_at
        }

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        if not isinstance(action, str):
            raise InvalidType('action')

        action = action.strip()
        if not action:
            raise RequiredValue('action')

        if action not in ['desk_download_users', 'send_ticket_transcription', 'desk_download_use_report']:
            raise InvalidValue('action')

        self.__action = action

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, account_id):
        if not isinstance(account_id, str):
            raise InvalidType('account id')

        action = account_id.strip()
        if not action:
            raise EmptyObject('account id')

        self.__account_id = account_id

    @property
    def requester_id(self):
        return self.__requester_id

    @requester_id.setter
    def requester_id(self, requester_id):
        if not isinstance(requester_id, str):
            raise InvalidType('requester id')

        requester_id = requester_id.strip()
        if not requester_id:
            raise EmptyObject('requester id')

        self.__requester_id = requester_id

    @property
    def info(self):
        return self.__info

    @property
    def info_encoded(self):
        return encode_obj(self.__info)

    @info.setter
    def info(self, info):
        format_info = {}
        if self.action in ['desk_download_users', 'send_ticket_transcription','desk_download_use_report']:
            if not info:
                raise RequiredValue('info')

            if not isinstance(info, dict):
                raise InvalidType('info')

            if self.action == 'desk_download_users':
                format_info = InfoDownloadUsers(info).data

            elif self.action == 'send_ticket_transcription':
                format_info = InfoTicketSendTranscription(**info).data
            
            elif self.action == 'desk_download_use_report':
                format_info = InfoDownloadUseReport(**info).data

        self.__info = format_info
