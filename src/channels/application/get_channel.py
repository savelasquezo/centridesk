from shared.exceptions.not_found import NotFound


class GetChannel:
    def __init__(self, channel_id, channels_obj):
        self.channel_id = channel_id
        self.channels_obj = channels_obj

    def get(self):
        self.channels_obj.channel_id = self.channel_id
        channel = self.channels_obj.get_by_id()

        if not channel:
            raise NotFound('channel')

        return channel
