from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced


class AccountsDatabaseMysql:

    def __init__(self, account_id=None):
        self.__db = MysqlConnBalanced('centridesk_admin')
        self.account_id = account_id

    def check_account_db_exists(self):
        return self.__db.check_database_exists(f"centridesk_{self.account_id}")

    def create_db(self):
        # create database
        sql = f"CREATE DATABASE IF NOT EXISTS centridesk_{self.account_id};"
        self.__db.execute_and_commit(sql)

        # give privileges to centridesk user
        privileges = f"GRANT ALL PRIVILEGES ON `centridesk_{self.account_id}`.* " \
                     f"TO 'centridesk_user'@'%';"
        self.__db.execute_and_commit(privileges)

    def drop_db(self):
        self.__db.drop_database(f"centridesk_{self.account_id}")

    def create_tables(self):
        self.create_customers_table()
        self.create_tickets_table()
        self.create_comments_tables()
        self.create_actions_table()
        self.create_configurations_table()

    def create_customers_table(self):
        sql = f"CREATE TABLE IF NOT EXISTS `centridesk_{self.account_id}`.`customers` (" \
              f"`id` int(11) NOT NULL AUTO_INCREMENT," \
              f"`unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`agent_id` varchar(255) DEFAULT NULL," \
              f"`display_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`centribot_external_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`external_id` longtext DEFAULT NULL," \
              f"`company` varchar(255) DEFAULT NULL," \
              f"`delegation` longtext DEFAULT NULL," \
              f"`gdpr` tinyint(1) NOT NULL DEFAULT 1," \
              f"`gdpr_updated_at` bigint(20) DEFAULT NULL," \
              f"`last_comment_at` bigint(20) DEFAULT NULL," \
              f"`created_at` bigint(20) NOT NULL," \
              f"`updated_at` bigint(20) DEFAULT NULL," \
              f"`active` tinyint(1) NOT NULL DEFAULT 1," \
              f"PRIMARY KEY (`id`)," \
              f"UNIQUE KEY `unique_id` (`unique_id`)" \
              f");"
        self.__db.execute_and_commit(sql)

    def create_tickets_table(self):
        sql = f"CREATE TABLE IF NOT EXISTS `centridesk_{self.account_id}`.`tickets` (" \
              f"`id` int(11) NOT NULL AUTO_INCREMENT," \
              f"`unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`title` longtext NOT NULL," \
              f"`assignee_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`author_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`is_agent` tinyint(1) DEFAULT 0," \
              f"`priority_id` int(11) NOT NULL," \
              f"`status_id` int(11) NOT NULL," \
              f"`external_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`channel_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`centribot_channel_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`centribot_project_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL," \
              f"`tags` longtext DEFAULT NULL," \
              f"`active` tinyint(1) NOT NULL DEFAULT 1," \
              f"`created_at` bigint(20) NOT NULL," \
              f"`updated_at` bigint(20) DEFAULT NULL," \
              f"`closed_at` bigint(20) DEFAULT NULL," \
              f"PRIMARY KEY (`id`)," \
              f"UNIQUE KEY `unique_id` (`unique_id`)," \
              f"KEY `status_id` (`status_id`)," \
              f"KEY `created_at` (`created_at`)" \
              f");"
        self.__db.execute_and_commit(sql)

    def create_comments_tables(self):
        sql = f"CREATE TABLE IF NOT EXISTS `centridesk_{self.account_id}`.`comments` (" \
              f"`id` bigint(20) NOT NULL AUTO_INCREMENT," \
              f"`unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`text` longtext COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`text_json` longtext default NULL," \
              f"`attachments` longtext DEFAULT NULL," \
              f"`author_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`is_agent` tinyint(1) DEFAULT 0," \
              f"`public` tinyint(1) DEFAULT 1," \
              f"`ticket_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`created_at` bigint(20) NOT NULL," \
              f"PRIMARY KEY (`id`)," \
              f"UNIQUE KEY `unique_id` (`unique_id`)," \
              f"KEY `ticket_id` (`ticket_id`)" \
              f");"
        self.__db.execute_and_commit(sql)

    def create_actions_table(self):
        sql = f"CREATE TABLE IF NOT EXISTS `centridesk_{self.account_id}`.`actions` (" \
              f"`id` int(11) NOT NULL AUTO_INCREMENT," \
              f"`unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL," \
              f"`action` varchar(255) NOT NULL," \
              f"`requester_id` varchar(255) NOT NULL," \
              f"`pending` tinyint(1) NOT NULL DEFAULT 0," \
              f"`in_progress` tinyint(1) NOT NULL DEFAULT 1," \
              f"`result` int(11) NOT NULL," \
              f"`error` longtext DEFAULT NULL,"\
              f"`info` longtext DEFAULT NULL," \
              f"`created_at` bigint(20) NOT NULL," \
              f"`initiated_at` bigint(20) DEFAULT NULL," \
              f"`finished_at` bigint(20) DEFAULT NULL," \
              f"PRIMARY KEY (`id`)," \
              f"UNIQUE KEY `unique_id` (`unique_id`)" \
              f");"
        self.__db.execute_and_commit(sql)

    def create_configurations_table(self):
        sql = f"CREATE TABLE IF NOT EXISTS `centridesk_{self.account_id}`.`configurations` (" \
              f"`id` int(11) NOT NULL AUTO_INCREMENT," \
              f"`name` varchar(255) NOT NULL," \
              f"`info` longtext DEFAULT NULL," \
              f"`created_at` bigint(20) NOT NULL," \
              f"`updated_at` bigint(20) DEFAULT NULL," \
              f"PRIMARY KEY (`id`)," \
              f"UNIQUE KEY `name` (`name`)" \
              f");"
        self.__db.execute_and_commit(sql)
