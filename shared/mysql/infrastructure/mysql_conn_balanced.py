import os
from time import sleep

import mysql.connector

from shared.infrastructure.get_config import GetConfig


class MysqlConnBalanced:

    def __init__(self, db_name=None, timezone=None, db=None):
        self.db_name = db_name
        self.timezone = timezone or 'Europe/Madrid'
        self.credentials = self.__get_credentials()
        self.db = db
        self.__conn = None
        self.__pooled = None
        self.__cursor = None
        self.__pool = GetConfig().get("db.pool")

    def __get_credentials(self):
        try:
            db = GetConfig().get(f"db.{self.db_name}")
        except Exception as ex:
            raise Exception(f"Error getting database credentials \bDBName: {self.db_name}. \nException: {ex}")

        return db

    def __get_conn_simple(self, master=True, pool=True):
        credentials = self.credentials.master if master else self.credentials.slave

        if pool and self.credentials.pool and os.environ.get('OTEL_SERVICE_NAME') == 'centridesk':
            self.__pooled = mysql.connector.connect(
                pool_name='-'.join([self.__pool.name, credentials['dbname'],'master' if master else 'reader']),
                pool_size=self.__pool.size,
                use_pure=self.__pool.use_pure if hasattr(self.__pool,"use_pure") else False,
                host=credentials['host'],
                user=credentials['user'],
                passwd=credentials['password'],
                database=credentials['dbname']
            )
            self.__conn = self.__pooled._cnx

        else:
            self.__conn = mysql.connector.connect(
                use_pure=self.__pool.use_pure if hasattr(self.__pool,"use_pure") else False,
                host=credentials['host'],
                user=credentials['user'],
                passwd=credentials['password'],
                database=credentials['dbname']
            )
            self.__pooled = None

        self.__conn.time_zone = self.timezone
        self.__cursor = self.__conn.cursor(buffered=True, dictionary=True)

    def __get_conn(self, master=True):
        retry_errors_list = [
            'Lost connection to MySQL server during query',
            'MySQL server has gone away',
            'MySQL Connection not available'
        ]

        retry, counter, max_retries = True, 0, 2

        while retry and counter < max_retries:
            counter += 1
            try:
                self.__get_conn_simple(master=master, pool=(counter == 1))
                retry = False

            except Exception as e:
                self.__close()
                if counter == max_retries:
                    raise e

                if any(err in str(e) for err in retry_errors_list):
                    sleep(1)

                else:
                    raise e

    def execute_and_commit(self, sql, params=()):
        try:
            self.__get_conn()
            self.__cursor.execute(sql, params)
            self.__conn.commit()
            row_id = self.__cursor.lastrowid
            self.__close()

        except Exception as ex:
            raise Exception(f"Query: {sql} \nParams: {params} \nError: {ex}")

        return row_id

    def execute_and_fetchall(self, sql):
        try:
            self.__get_conn(master=False)
            self.__cursor.execute(sql)
            output = self.__cursor.fetchall()
            self.__close()

        except Exception as ex:
            raise Exception(f"Query: {sql}\nError: {ex}")

        return output

    def execute_and_fetchone(self, sql):
        try:
            self.__get_conn(master=False)
            self.__cursor.execute(sql)
            output = self.__cursor.fetchone()
            self.__close()

        except Exception as ex:
            raise Exception(f"Query: {sql}\nError: {ex}")

        return output

    def __close(self):
        try:
            if self.__conn and self.__conn.is_connected():
                self.__cursor.close()
                if self.__pooled:
                    self.__pooled.close()
                else:
                    self.__conn.close()
        except Exception as e:
            raise Exception(f"Error closing mysql connection, Error: {e}")

    def check_table_exists(self, table_name):
        sql = f"show tables like '{table_name}';"
        exists = self.execute_and_fetchone(sql)

        return exists or False

    def truncate_table(self, table_name):
        if self.check_table_exists(table_name):
            sql = f"truncate table `{table_name}`;"
            self.execute_and_commit(sql)

    def drop_table(self, table_name):
        if self.check_table_exists(table_name):
            sql = f"drop table `{table_name}`;"
            self.execute_and_commit(sql)

    def check_database_exists(self, db_name):
        sql = f"show databases like '{db_name}';"
        return self.execute_and_fetchone(sql) or False

    def drop_database(self, db_name):
        if self.check_database_exists(db_name):
            sql = f"drop database `{db_name}`;"
            self.execute_and_commit(sql)

    def show_databases_like(self, like):
        sql = f"show databases like '%{like}%';"
        return self.execute_and_fetchall(sql)
