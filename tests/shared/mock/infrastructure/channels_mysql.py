from src.channels.domain.channel import Channel
from tests.shared.mock.data import MockData


class ChannelsMysql:

    def __init__(self, channel_id=None, platform=None, mock=None):
        self.channel_id = channel_id
        self.platform = platform

        self.mock = mock or MockData()

    def get_all(self):
        return [Channel(c).data for c in self.mock.channels]

    def get_by_platform(self):
        for channel in self.mock.channels:
            if channel['platform'] == self.platform:
                return Channel(channel).data

    def get_by_id(self):
        for channel in self.mock.channels:
            if channel['unique_id'] == self.channel_id:
                return Channel(channel).data
