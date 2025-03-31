import ffmpeg

from shared.files.infrastructure.file_converter import FileConverter


class VideoConverter(FileConverter):

    def __init__(self, filepath=None):
        super().__init__('mp4', filepath)

        self.__rotation = None
        self.__width = None
        self.__height = None
        self.__o = None
        self.__r = None

    def has_to_convert(self):
        stream = self.get_stream()

        convert_audio = convert_video = False
        for s in stream:
            if s['codec_type'] == 'audio':
                if s['codec_name'] != self.VALID_VIDEO_CODEC_AUDIO:
                    convert_audio = True

            elif s['codec_type'] == 'video':
                if s['codec_name'] != self.VALID_VIDEO_CODEC_VIDEO:
                    convert_video = True

                for i in s.get('side_data_list', []):
                    if i.get('side_data_type') == 'Display Matrix':
                        self.__rotation = i.get('rotation', None)

                self.__width = s['width']
                self.__height = s['height']

        if self.filepath.split('.')[-1] != self.extension:
            convert_video = True

        return convert_audio or convert_video

    def has_to_resize(self):
        ratio_16_9 = round(16 / 9, 3)
        ratio_4_3 = round(4 / 3, 3)

        ratios_resolutions = {
            '16:9': {'short': 360, 'long': 640},
            '4:3': {'short': 480, 'long': 640},
            'other': {'max': 1280}
        }

        if self.__width >= self.__height:
            self.__o = 'h'
            ratio = self.__width / self.__height

        else:
            self.__o = 'v'
            ratio = self.__height / self.__width

        ratio = round(ratio, 3)

        resize = False
        if ratio == ratio_16_9:
            self.__r = ratios_resolutions['16:9']

            if self.__o == 'h':
                if self.__width > self.__r['long']:
                    resize = True

            else:
                if self.__height > self.__r['long']:
                    resize = True

        elif ratio == ratio_4_3:
            self.__r = ratios_resolutions['4:3']

            if self.__o == 'h':
                if self.__width > self.__r['long']:
                    resize = True

            else:
                if self.__height > self.__r['long']:
                    resize = True

        else:
            self.__r = ratios_resolutions['other']

            if self.__o == 'h':
                if self.__width > self.__r['max']:
                    self.__r['long'] = self.__r['max']
                    self.__r['short'] = round(self.__height * self.__r['max'] / self.__width / 2) * 2

                    resize = True

            else:
                if self.__r['max'] < self.__height:
                    self.__r['long'] = self.__r['max']
                    self.__r['short'] = round(self.__width * self.__r['max'] / self.__height / 2) * 2

                    resize = True

        return resize

    def convert(self):
        (
            ffmpeg
            .input(self.filepath)
            .output(self.converted_filepath, vcodec='h264', acodec='aac')
            .run()
        )

    def convert_and_resize(self):
        # size to ffmpeg WxH
        if self.__rotation in [-90, 90, 270]:
            size = f"{self.__r['short']}x{self.__r['long']}" if self.__o == 'h' else f"{self.__r['long']}x{self.__r['short']}"
        else:
            size = f"{self.__r['long']}x{self.__r['short']}" if self.__o == 'h' else f"{self.__r['short']}x{self.__r['long']}"

        (
            ffmpeg
            .input(self.filepath)
            .output(self.converted_filepath, vcodec='h264', acodec='aac', **{'s': size})
            .run()
        )
