from shared.mysql.infrastructure.mysql_methods import MysqlMethods


class CentrideskMysql(MysqlMethods):

    def __init__(self):
        self.db_name = 'centridesk'
        super().__init__(db_name=self.db_name)
