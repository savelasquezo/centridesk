from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class URL:

    def __init__(self, url):
        self.url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if url is None:
            raise RequiredValue('url')

        if not isinstance(url, str):
            raise TypeErrorValue('url')

        url = url.strip()
        if not url:
            raise RequiredValue('url')

        if not url.startswith("https://"):
            raise InvalidValue('url')

        self.__url = url
