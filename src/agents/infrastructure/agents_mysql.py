from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced
from src.agents.domain.agent_out import AgentOut


class AgentsMysql:

    def __init__(self, agent_id=None, account_id=None):
        self.agent_id = agent_id
        self.account_id = account_id

        self.__db = MysqlConnBalanced('centribot')

    def get_by_id(self):
        sql = f"select cu.unique_id, cu.lang, au.first_name, au.last_name, au.email, au.is_active, cu.created_at, " \
              f"cu.updated_at, cu.deactivated_at, cu.desk " \
              f"from `centribot`.`auth_user` au, `centribot`.`api_catuser` cu " \
              f"where au.id = cu.user_id " \
              f"and cu.unique_id = '{self.agent_id}';"

        return AgentOut(self.__db.execute_and_fetchone(sql)).data

    def get_account(self):
        sql = f"select user_id, account_id " \
              f"from `centribot`.`api_usersaccounts` " \
              f"where user_id = '{self.agent_id}';"
        return self.__db.execute_and_fetchone(sql)

    def get_user_account_by_user_and_account(self):
        sql = f"select id, user_id, account_id " \
              f"from `centribot`.`api_usersaccounts` " \
              f"where user_id = '{self.agent_id}' and account_id = '{self.account_id}';"
        return self.__db.execute_and_fetchone(sql)

    def get_user_rol_by_user(self):
        sql = f"select id, user_id, role_id " \
              f"from `centribot`.`api_usersroles` " \
              f"where user_id = '{self.agent_id}';"
        return self.__db.execute_and_fetchone(sql)

    def get_role(self, role_id):
        sql = f"select id, unique_id, name, bot, desk " \
              f"from `centribot`.`api_roles` " \
              f"where unique_id = '{role_id}';"
        return self.__db.execute_and_fetchone(sql)

    def get_by_username(self, username):
        sql = f"select cu.unique_id, cu.lang, au.first_name, au.last_name, au.email, au.is_active, cu.created_at, " \
              f"cu.updated_at, cu.deactivated_at, cu.desk " \
              f"from `centribot`.`auth_user` au, `centribot`.`api_catuser` cu " \
              f"where au.id = cu.user_id " \
              f"and au.username = '{username}';"

        return AgentOut(self.__db.execute_and_fetchone(sql)).data

    def get_rol_by_user(self):
        sql = f"select ur.user_id, ur.role_id, r.name, r.bot, r.desk " \
              f"from `centribot`.`api_usersroles` ur, `centribot`.`api_roles` r " \
              f"where ur.user_id = '{self.agent_id}' " \
              f"and r.unique_id = ur.role_id;"

        return self.__db.execute_and_fetchone(sql)    
    # Agents    
    def list_agents(self):
        sql = f"select au.username, c.unique_id, au.first_name, au.last_name " \
              f"from centribot.api_accounts a, centribot.api_usersaccounts ua, centribot.api_usersroles ur, centribot.api_catuser c, centribot.auth_user au " \
              f"where a.unique_id = ua.account_id " \
              f"and ua.user_id = ur.user_id " \
              f"and c.unique_id = ua.user_id " \
              f"and c.user_id = au.id " \
              f"and account_id = '{self.account_id}';"

        return self.__db.execute_and_fetchall(sql)
