from src.configurations.infrastructure.transcriptions_mysql import TranscriptionsMysql

from shared.exceptions.generic import GenericException
from shared.exceptions.not_found import NotFound


class Transcriptions:

    def __init__(self, account_id, transcriptions_obj: TranscriptionsMysql, info=None) -> None:
        self.account_id = account_id
        self.info = info
        self.transcriptions_obj = transcriptions_obj

    def create(self):
        self.transcriptions_obj.account_id = self.account_id
        self.transcriptions_obj.info = self.info

        if self.transcriptions_obj.get_by_key():
            raise GenericException('Transcription already exists')

        return self.transcriptions_obj.create()

    def get(self):
        self.transcriptions_obj.account_id = self.account_id
        return self.transcriptions_obj.get_by_key()

    def update(self):
        self.transcriptions_obj.account_id = self.account_id
        self.transcriptions_obj.info = self.info

        if not self.transcriptions_obj.get_by_key():
            raise NotFound('transcription')

        self.transcriptions_obj.update_by_key()

        return self.transcriptions_obj.get_by_key()
