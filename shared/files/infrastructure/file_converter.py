import ffmpeg
from abc import abstractmethod


class FileConverter:
    VALID_AUDIO_CODEC = 'mp3'

    VALID_VIDEO_CODEC_AUDIO = 'aac'
    VALID_VIDEO_CODEC_VIDEO = 'h264'

    def __init__(self, extension, filepath=None):
        self.extension = extension
        self.filepath = filepath

    @property
    def converted_filepath(self):
        p = self.filepath.split('.')
        return p[0] + '_converted.' + self.extension

    def get_stream(self):
        return ffmpeg.probe(self.filepath)['streams']

    @abstractmethod
    def has_to_convert(self):
        pass

    @abstractmethod
    def has_to_resize(self):
        pass

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def convert_and_resize(self):
        pass
