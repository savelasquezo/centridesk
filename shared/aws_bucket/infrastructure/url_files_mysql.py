from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced


class UrlFilesMysql:

    def __init__(self, file_type=None):
        self.__db = MysqlConnBalanced('centribot')
        self.file_type = file_type

    def get(self):
        sql = f"select type, base_url, bucket_name " \
              f"from api_defaulturlfiles " \
              f"where type = '{self.file_type}';"
        return self.__db.execute_and_fetchone(sql)

    def save_conversation_url(self, url, created_at):
        sql = f"insert into api_conversationsurls (url, created_at) " \
              f"values ('{url}', {created_at})"
        self.__db.execute_and_commit(sql)
