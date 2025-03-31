from argparse import ArgumentParser
from os import path as os_path
from sys import path as sys_path, exit

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from shared.mysql.infrastructure.mysql_conn_balanced import MysqlConnBalanced

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-a", "--apply", action='store_true', help="Apply changes")
    parser.add_argument("-r", "--rollback", action='store_true', help="Rollback Changes")
    args = parser.parse_args()

    db = MysqlConnBalanced('centridesk_admin')
    databases = db.show_databases_like('centridesk_')

    query1 = ""
    query2 = ""
    if args.apply:
        print('Apply Changes')
        query1 = "alter table $DBNAME.customers add column `agent_id` varchar(255) DEFAULT NULL after unique_id;"
        query2 = "alter table $DBNAME.customers add column `company` varchar(255) DEFAULT NULL after external_id;"
    elif args.rollback:
        print('Rollback')
        query1 = "alter table $DBNAME.customers drop column `agent_id`"
        query2 = "alter table $DBNAME.customers drop column `company`"
    else:
        exit(0)

    for database in databases:
        try:
            database_name = list(database.values())[0]
            if database_name != 'centridesk_shared':
                sql1 = query1.replace('$DBNAME', database_name)
                print(sql1)
                db.execute_and_commit(sql1)
                sql2 = query2.replace('$DBNAME', database_name)
                print(sql2)
                db.execute_and_commit(sql2)

        except Exception as ex:
            print(ex)
