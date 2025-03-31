from shared.infrastructure.b64 import decode_obj, encode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date, get_timestamp
from src.actions.domain.action_in import Action
from tests.shared.mock.data import MockData


class ActionsMysql:
    def __init__(self, account_id=None, action_id=None, mock=None):
        self.__mock = mock or MockData()
        self.account_id = account_id
        self.action_id = action_id

    def create(self, action: Action):
        output = {
            "id": action.unique_id,
            "action": action.action,
            "requester_id": action.requester_id,
            "info": action.info_encoded,
            "pending": action.pending,
            "in_progress": action.in_progress,
            "result": action.result,
            "error": None,
            "created_at": action.created_at,
            "initiated_at": None,
            "finished_at": None
        }

        self.__mock.actions.get(self.account_id, []).append(output)

        return self.__format(output)

    def get_by_id(self):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['id'] == self.action_id:
                output = self.__format(action)
                break

        return output

    def get_by_pending(self, pending):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['pending'] == pending:
                output = self.__format(action)
                break

        return output

    def get_by_in_progress(self, in_progress):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['in_progress'] == in_progress:
                output = self.__format(action)
                break

        return output

    def delete_by_id(self):
        output = False
        for action in self.__mock.actions.get(self.account_id, []):
            if action['id'] == self.action_id:
                output = True
                break

        return output

    def update_initiated(self):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['id'] == self.action_id:
                output = action
                break
        output['initiated_at'] = get_timestamp()
        output['pending'] = 0
        output['in_progress'] = 1

    def update_finished(self):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['id'] == self.action_id:
                output = action
                break
        output['finished_at'] = get_timestamp()
        output['pending'] = 1
        output['in_progress'] = 0

    def update_error(self, error):
        output = None
        for action in self.__mock.actions.get(self.account_id, []):
            if action['id'] == self.action_id:
                output = action
                break
        output['finished_at'] = get_timestamp()
        output['result'] = 2
        output['in_progress'] = 0
        output['pending'] = 0
        output['error'] = encode_obj(f"{error}")

    @staticmethod
    def __format(value):
        output = {
            'id': value['id'],
            "action": value['action'],
            "requester_id": value['requester_id'],
            "pending": value['pending'],
            "in_progress": value['in_progress'],
            "result": value['result'],
            "error": decode_obj(value['error']),
            "info": decode_obj(value['info']),
            "created_at": from_timestamp_to_date(value['created_at']),
            "initiated_at": from_timestamp_to_date(value['initiated_at']),
            "finished_at": from_timestamp_to_date(value['finished_at'])
        }

        return output
