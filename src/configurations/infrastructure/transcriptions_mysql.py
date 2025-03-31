from src.configurations.infrastructure.configurations_mysql import ConfigurationsMysql


class TranscriptionsMysql(ConfigurationsMysql):
    def __init__(self, account_id=None, info=None):
        super().__init__(key='transcriptions', account_id=account_id, info=info)
