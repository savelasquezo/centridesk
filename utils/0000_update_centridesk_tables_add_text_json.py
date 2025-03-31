from argparse import ArgumentParser
from os import path as os_path
from sys import path as sys_path

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-a", "--apply", action='store_true', help="Apply changes")
    parser.add_argument("-r", "--rollback", action='store_true', help="Rollback Changes")
    args = parser.parse_args()

    query = ""

    if args.apply:
        print('Apply Changes')
        query = f"alter table $DBNAME.comments add column text_json longtext DEFAULT NULL after `text`;"
    elif args.rollback:
        print('Rollback')
        query = f"alter table $DBNAME.comments drop column text_json;"
    else:
        print('Nothing to do.')
        exit(0)

    db = MysqlConnBalanced('centridesk_admin')
    databases = db.show_databases_like('centridesk_')

    for database in databases:
        try:
            database_name = list(database.values())[0]
            if database_name != 'centridesk_shared':
                sql1 = query.replace('$DBNAME', database_name)
                print(sql1)
                db.execute_and_commit(sql1)

        except Exception as ex:
            print(ex)
