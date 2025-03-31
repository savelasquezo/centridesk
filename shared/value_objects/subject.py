from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class Subject:

    def __init__(self, subject):
        self.__name = 'subject'
        self.subject = subject

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        if not isinstance(subject, str):
            raise TypeErrorValue(self.__name)

        subject = subject.strip()
        if not subject:
            raise RequiredValue(self.__name)

        self.__subject = subject
