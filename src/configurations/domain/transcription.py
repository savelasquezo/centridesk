from shared.value_objects.email import Email
from shared.infrastructure.b64 import encode_obj


class Transcription:

    def __init__(self, email) -> None:
        self.email = email

    @property
    def data(self):
        return {'email': self.email}

    @property
    def encoded(self):
        return encode_obj(self.data)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = Email(value).email
