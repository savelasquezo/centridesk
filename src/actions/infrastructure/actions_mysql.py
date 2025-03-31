from shared.infrastructure.b64 import encode_obj
from shared.infrastructure.timestamps import get_timestamp
from shared.mysql.infrastructure.centridesk import CentrideskMysql
from src.actions.domain.action_in import Action
from src.actions.domain.action_out import ActionOut


class ActionsMysql(CentrideskMysql):
    def __init__(self, account_id=None, action_id=None):
        super().__init__()
        self.account_id = account_id
        self.action_id = action_id

        self.__table = 'actions'
        self.__opts = ['id', 'unique_id', 'action', 'requester_id', 'info', 'pending', 'in_progress', 'result', 'error',
                       'created_at', 'initiated_at', 'finished_at']

    def create(self, action: Action):
        params = {
            'unique_id': action.unique_id,
            'action': action.action,
            'requester_id': action.requester_id,
            'info': action.info_encoded,
            'pending': action.pending,
            'in_progress': action.in_progress,
            'result': action.result,
            'created_at': action.created_at
        }

        return self.insert(self.account_id, self.__table, params=params)

    def get_by_id(self):
        conditions = {'unique_id': {'op': '=', 'value': self.action_id}}
        action = self.select_one(self.account_id, self.__table, self.__opts, conditions)
        return ActionOut(action).data

    def get_by_pending(self, pending):
        conditions = {'pending': {'op': '=', 'value': pending}}
        action = self.select_one(self.account_id, self.__table, self.__opts, conditions)
        return ActionOut(action).data

    def get_by_in_progress(self, in_progress):
        conditions = {'in_progress': {'op': '=', 'value': in_progress}}
        action = self.select_one(self.account_id, self.__table, self.__opts, conditions)
        return ActionOut(action).data

    def delete_by_id(self):
        condition = {'unique_id': {'op': '=', 'value': self.action_id}}
        self.delete(self.account_id, self.__table, conditions=condition)

    def update_initiated(self):
        params = {'initiated_at': get_timestamp(), 'pending': 0, 'in_progress': 1}
        condition = {'unique_id': {'op': '=', 'value': self.action_id}}
        self.update(self.account_id, self.__table, params=params, conditions=condition)

    def update_finished(self):
        params = {'finished_at': get_timestamp(), 'result': 1, 'in_progress': 0}
        condition = {'unique_id': {'op': '=', 'value': self.action_id}}
        self.update(self.account_id, self.__table, params=params, conditions=condition)

    def update_error(self, error):
        params = {
            'finished_at': get_timestamp(),
            'result': 2,
            'in_progress': 0,
            'pending': 0,
            'error': encode_obj(f"{error}")
        }
        condition = {'unique_id': {'op': '=', 'value': self.action_id}}
        self.update(self.account_id, self.__table, params=params, conditions=condition)
