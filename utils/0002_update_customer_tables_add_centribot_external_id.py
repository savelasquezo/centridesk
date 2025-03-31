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
    query3 = ""
    query4 = ""
    if args.apply:
        print('Apply Changes')
        query1 = "alter table $DBNAME.customers add column `centribot_external_id` varchar(255) default null after " \
                 "`phone`;"
        query2 = "update $DBNAME.customers set `centribot_external_id` = `external_id`;"
        query3 = "update $DBNAME.customers set `external_id` = null;"
        query4 = "alter table $DBNAME.customers modify column `external_id` longtext default null;"
    elif args.rollback:
        print('Rollback')
        query1 = "update $DBNAME.customers set `external_id` = null;"
        query2 = "alter table $DBNAME.customers modify column `external_id` varchar(255) default null ;"
        query3 = "update $DBNAME.customers set `external_id` = `centribot_external_id`;"
        query4 = "alter table $DBNAME.customers drop column `centribot_external_id`"
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
                sql3 = query3.replace('$DBNAME', database_name)
                print(sql3)
                db.execute_and_commit(sql3)
                sql4 = query4.replace('$DBNAME', database_name)
                print(sql4)
                db.execute_and_commit(sql4)

        except Exception as ex:
            print(ex)
