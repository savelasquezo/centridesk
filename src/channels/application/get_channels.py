class GetChannels:

    def __init__(self, channels_obj):
        self.channels_obj = channels_obj

    def get(self):
        return self.channels_obj.get_all()
