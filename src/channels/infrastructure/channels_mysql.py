from src.channels.domain.channel import Channel
from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced


class ChannelsMysql:

    def __init__(self, channel_id=None, platform=None):
        self.channel_id = channel_id
        self.platform = platform

        self.__db = MysqlConnBalanced('centridesk')

    def get_all(self):
        sql = f"select unique_id, name, platform, created_at, active " \
              f"from api_channels;"
        channels = self.__db.execute_and_fetchall(sql)
        return [Channel(c).data for c in channels]

    def get_by_platform(self):
        sql = f"select unique_id, name, platform, created_at, active " \
              f"from api_channels " \
              f"where platform = '{self.platform}';"
        channel = self.__db.execute_and_fetchone(sql)
        return Channel(channel).data

    def get_by_id(self):
        sql = f"select unique_id, name, platform, created_at, active " \
              f"from api_channels " \
              f"where unique_id = '{self.channel_id}';"
        channel = self.__db.execute_and_fetchone(sql)
        return Channel(channel).data
