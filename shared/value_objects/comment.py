from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class CommentBody:

    def __init__(self, text):
        self.__name = 'text'
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if text and not isinstance(text, str):
            raise TypeErrorValue(self.__name)

        if not text or not text.strip():
            raise RequiredValue(self.__name)

        self.__text = text
