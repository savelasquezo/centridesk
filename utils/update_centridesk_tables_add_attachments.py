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
        query = f"alter table centridesk_$ACCOUNT_ID.comments add column attachments longtext DEFAULT NULL after `text`;"
    elif args.rollback:
        print('Rollback')
        query = f"alter table centridesk_$ACCOUNT_ID.comments drop column attachments;"
    else:
        print('Nothing to do.')
        exit(0)

    db1 = MysqlConnBalanced('centribot')
    sql = "select account_id from api_accountsplatformproducts where centridesk = 1;"
    accounts = db1.execute_and_fetchall(sql)

    for account in accounts:
        try:
            db2 = MysqlConnBalanced(f"centridesk_admin")
            db2.execute_and_commit(query.replace('$ACCOUNT_ID', account['account_id']))

        except Exception as ex:
            print(ex)
