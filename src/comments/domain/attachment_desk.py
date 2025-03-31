from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.too_big_number import TooBigNumber
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.url import URL


class AttachmentDesk:
    __VALID_EXTENSIONS = ['3g2', '3gp', '7z', 'aac', 'amr', 'avi', 'bmp', 'csv', 'docx', 'eml', 'gif', 'heic',
                          'heif', 'ics', 'jfif', 'jpeg', 'jpg', 'key', 'log', 'm4a', 'm4v', 'mov', 'mp3', 'mp4', 'mp4a',
                          'mpeg', 'mpg', 'mpga', 'neon', 'numbers', 'odt', 'oga', 'ogg', 'ogv', 'opus', 'pages', 'pdf',
                          'png', 'pps', 'ppsx', 'ppt', 'pptx', 'qt', 'svg', 'tif', 'tiff', 'txt', 'vcf', 'wav', 'webm',
                          'webp', 'wmv', 'xls', 'xlsx', 'xml', 'yaml', 'yml', 'zip']

    __DOCUMENT_VALID_MIME_TYPES = [
        'text/plain',
        'application/pdf',
        'application/vnd.ms-powerpoint',
        'application/msword',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    __DOCUMENT_SIZE_LIMIT = 52428800  # 100Mb

    __AUDIO_VALID_MIME_TYPES = [
        'audio/aac',
        'audio/mp4',
        'audio/mpeg',
        'audio/amr',
        'audio/ogg',
    ]
    __AUDIO_SIZE_LIMIT = 16777216  # 16Mb

    __VIDEO_VALID_MIME_TYPES = [
        'video/mp4',
        'video/3gp'
    ]
    __VIDEO_SIZE_LIMIT = 167772160  # 160Mb

    __IMAGE_VALID_MIME_TYPES = [
        'image/jpeg', 'image/png'
    ]
    __IMAGE_SIZE_LIMIT = 5242880  # 5Mb

    __STICKER_VALID_MIME_TYPES = [
        'image/webp'
    ]
    __STICKER_SIZE_LIMIT = 102400  # 100kB

    __MEDIA_SIZE_LIMIT = {
        'document': __DOCUMENT_SIZE_LIMIT,
        'audio': __AUDIO_SIZE_LIMIT,
        'video': __VIDEO_SIZE_LIMIT,
        'image': __IMAGE_SIZE_LIMIT,
        'sticker': __STICKER_SIZE_LIMIT
    }

    def __init__(self, filename, type, mediatype, content, mediasize, url=None, filetype=None):
        self.filetype = filetype
        self.filename = filename
        self.type = type
        self.mediatype = mediatype
        self.content = content
        self.mediasize = mediasize
        self.url = url

    @property
    def data(self):
        return {
            'filename': self.filename,
            'type': self.type,
            'mediatype': self.mediatype,
            'filetype': self.filetype,
            'url': self.url,
            'mediasize': self.mediasize,
            'content': self.content
        }

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        if filename is None:
            raise RequiredValue('attachment (filename)')

        if not isinstance(filename, str):
            raise TypeErrorValue('attachment (filename)')

        filename = filename.strip()
        if not filename:
            raise RequiredValue('attachment (filename)')

        if filename.split(".")[-1] not in self.__VALID_EXTENSIONS:
            raise InvalidValue('attachment (file extension)')

        self.__filename = filename

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
        if type not in ['image', 'file']:
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
        __t = mediatype.split('/')[0]

        self.filetype = 'document' if __t in ['text', 'application'] else __t
        # if not mediatype:
        #     raise RequiredValue('attachment (mediatype)')
        #
        # if mediatype in self.__DOCUMENT_VALID_MIME_TYPES:
        #     self.filetype = 'document'
        #
        # elif mediatype in self.__IMAGE_VALID_MIME_TYPES:
        #     self.filetype = 'image'
        #
        # elif mediatype in self.__VIDEO_VALID_MIME_TYPES:
        #     self.filetype = 'video'
        #
        # elif mediatype in self.__AUDIO_VALID_MIME_TYPES:
        #     self.filetype = 'audio'
        #
        # elif self.filetype in self.__STICKER_VALID_MIME_TYPES:
        #     self.filetype = 'sticker'
        #
        # else:
        #     raise InvalidValue('content Type')

        self.__mediatype = mediatype

    @property
    def filetype(self):
        return self.__filetype

    @filetype.setter
    def filetype(self, filetype):
        self.__filetype = filetype

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        if not content:
            raise RequiredValue('attachment (content)')

        if not isinstance(content, bytes):
            raise TypeErrorValue('attachment (content)')

        self.__content = content

    @property
    def mediasize(self):
        return self.__mediasize

    @mediasize.setter
    def mediasize(self, mediasize):
        if mediasize is None:
            raise RequiredValue('attachment (mediasize)')

        try:
            mediasize = int(mediasize)

            size_limit = self.__MEDIA_SIZE_LIMIT.get(self.filetype)

            if mediasize > size_limit:
                raise TooBigNumber('attachment (mediasize)', size_limit)

            self.__mediasize = mediasize

        except ValueError:
            raise TypeErrorValue('attachment (mediasize)')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = URL(url).url if url else None
