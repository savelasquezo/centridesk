import ffmpeg

from shared.files.infrastructure.file_converter import FileConverter


class AudioConverter(FileConverter):

    def __init__(self, filepath=None):
        super().__init__('mp3', filepath)

    def has_to_convert(self):
        stream = self.get_stream()

        convert_audio = False
        for s in stream:
            if s['codec_name'] != self.VALID_AUDIO_CODEC:
                convert_audio = True

        return convert_audio

    def has_to_resize(self):
        return False

    def convert(self):
        (
            ffmpeg
            .input(self.filepath)
            .output(self.converted_filepath, acodec='libmp3lame')
            .run()
        )

    def convert_and_resize(self):
        pass
