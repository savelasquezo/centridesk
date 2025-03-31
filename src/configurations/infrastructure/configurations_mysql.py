from shared.infrastructure.timestamps import get_timestamp
from shared.mysql.infrastructure.centridesk import CentrideskMysql
from src.configurations.domain.configuration_out import ConfigurationOut


class ConfigurationsMysql(CentrideskMysql):
    def __init__(self, account_id=None, key=None, info=None):
        super().__init__()
        self.account_id = account_id
        self.key = key
        self.info = info

        self.__table = 'configurations'
        self.__opts = ['info', 'created_at', 'updated_at']

    def create(self):
        created_at = get_timestamp()
        params = {
            'name': self.key,
            'info': self.info.encoded,
            'created_at': created_at
        }
        self.insert(self.account_id, self.__table, params)

        return ConfigurationOut(info=self.info.encoded, created_at=created_at).data

    def get_by_key(self):
        conditions = {'name': {'op': '=', 'value': self.key}}
        output = self.select_one(self.account_id, self.__table, self.__opts, conditions)

        return ConfigurationOut(**(output or {})).data

    def update_by_key(self):
        conditions = {'name': {'op': '=', 'value': self.key}}

        params = {
            'info': self.info.encoded,
            'updated_at': get_timestamp()
        }

        self.update(self.account_id, self.__table, params, conditions)
