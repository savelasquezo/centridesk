from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced


class AccountsMysql:

    def __init__(self, account_id=None):
        self.account_id = account_id

        self.__db = MysqlConnBalanced('centribot')

    def check_active(self):
        sql = f"select active " \
              f"from `centribot`.`api_accounts`  " \
              f"where unique_id = '{self.account_id}' ;"

        return self.__db.execute_and_fetchone(sql)

    def get_superadmin(self):
        sql = f"select ua.user_id, au.username, c.lang, a.to_reactivate " \
              f"from `centribot`.`api_accounts` a, `centribot`.`api_usersaccounts` ua, " \
              f"`centribot`.`api_usersroles` ur, `centribot`.`api_catuser` c, `centribot`.`auth_user` au " \
              f"where a.unique_id = ua.account_id " \
              f"and ua.user_id = ur.user_id and ur.role_id = 'c35851102cab49ff9d31e71c4a82b4e1' " \
              f"and c.unique_id = ua.user_id " \
              f"and c.user_id = au.id " \
              f"and account_id = '{self.account_id}';"

        return self.__db.execute_and_fetchone(sql)
