from shared.mysql.application.mysql_query_constructor import MysqlQueryConstructor
from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced


class MysqlMethods:

    def __init__(self, db_name):
        self.__base_name = 'centridesk'
        self.__query = MysqlQueryConstructor(db_name)
        self.__db = MysqlConnBalanced(db_name)

    def select_one(self, account_id, table, opts: list, conditions: dict = None):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.select(opts, conditions=conditions)
        return self.__db.execute_and_fetchone(sql)

    def select(self, account_id, table, opts: list, conditions: dict = None, order=None, limit=None, page=None,
               logic_operator: str = 'and'):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.select(opts, conditions=conditions, order=order, limit=limit, page=page,
                                  logic_operator=logic_operator)
        return self.__db.execute_and_fetchall(sql)

    def select_query(self, account_id, table, opts: list, query: list, order=None, limit=None, page=None):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.select_query(opts, query=query, order=order, limit=limit, page=page)
        return self.__db.execute_and_fetchall(sql)

    def insert(self, account_id, table, params):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.insert(params)
        return self.__db.execute_and_commit(sql, params=tuple(params.values()))

    def update(self, account_id, table, params, conditions=None):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.update(params, conditions)
        return self.__db.execute_and_commit(sql, params=tuple(params.values()))

    def delete(self, account_id, table, conditions=None):
        self.__query.db = self.__db.db = f'{self.__base_name}_{account_id}'
        self.__query.table = table
        sql = self.__query.delete(conditions)
        self.__db.execute_and_commit(sql)
