from os import path as os_path
from sys import path as sys_path

from traceback import print_exc

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced
from src.accounts.infrastructure.accounts_database_mysql import AccountsDatabaseMysql

if __name__ == '__main__':
    db = MysqlConnBalanced('centridesk_admin')
    databases = db.show_databases_like('centridesk_')

    accounts_obj = AccountsDatabaseMysql()

    for database in databases:
        try:
            database_name = list(database.values())[0]
            if database_name != 'centridesk_shared':
                account_id = database_name.replace('centridesk_', '')
                accounts_obj.account_id = account_id
                accounts_obj.create_actions_table()
                print(f'\033[0;32mCreating table for account {account_id}\033[0m')

        except:
            print('\033[0;31m')
            print_exc()
            print('\033[0m')
