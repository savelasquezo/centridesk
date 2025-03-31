from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.url import URL


class AttachmentSmooch:

    def __init__(self, type, mediatype, mediasize, url, filename=None):
        self.__attachment_valid_types = ['image', 'document', 'file']

        self.type = type
        self.mediatype = mediatype
        self.mediasize = mediasize
        self.url = url
        self.filename = filename

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        if type is None:
            raise RequiredValue('attachment (type)')

        if not isinstance(type, str):
            raise TypeErrorValue('attachment (type)')

        type = type.strip()
        if type not in self.__attachment_valid_types:
            raise InvalidValue('attachment (type)')

        self.__type = type

    @property
    def mediatype(self):
        return self.__mediatype

    @mediatype.setter
    def mediatype(self, mediatype):
        if mediatype is None:
            raise RequiredValue('attachment (mediatype)')

        if not isinstance(mediatype, str):
            raise TypeErrorValue('attachment (mediatype)')

        mediatype = mediatype.strip()
        if not mediatype:
            raise RequiredValue('attachment (mediatype)')

        self.__mediatype = mediatype

    @property
    def mediasize(self):
        return self.__mediasize

    @mediasize.setter
    def mediasize(self, mediasize):
        if mediasize is None:
            raise RequiredValue('attachment (mediasize)')

        self.__mediasize = mediasize

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = URL(url).url

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        self.__filename = value
