from pandas import DataFrame

from shared.customers.application.format_filter import format_filters
from shared.infrastructure.timestamps import get_timestamp
from src.accounts.infrastructure.accounts_mysql import AccountsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.generics.infrastructure.ep_create_upload_file import EntrypointCreateUploadFile


class EntrypointDownloadUsers:
    def __init__(self, account_id, info, requester_id):
        self.account_id = account_id
        self.info = info
        self.requester_id = requester_id
        self.__mail_template = 'desk_download_users'
        self.__send_email = True
        self.__file_name = f'{self.account_id}_{get_timestamp()}_users_desk.xlsx'
        self.__file_type = 'centridesk'
        self.__columns = ['name', 'email', 'phone', 'company', 'delegation', 'external_id', 'gdpr', 'gdpr_updated_at',
                          'agent_id', 'created_at']

    def run(self):
        # get account superadmin info
        account_obj = AccountsMysql(self.account_id)
        superadmin = account_obj.get_superadmin()

        # get filter users
        filter_by = format_filters(self.info['filter'])
        customers_obj = CustomersMysql(self.account_id)
        _df = DataFrame(customers_obj.filter(filter_by))
        _df = DataFrame(columns=self.__columns) if _df.empty else _df[self.__columns]

        ep_create_upload_file = EntrypointCreateUploadFile(
            dataframe={'Users': _df},
            file_name=self.__file_name,
            file_type=self.__file_type,
            superadmin=superadmin,
            requester_id=self.requester_id,
            send_email=self.__send_email,
            mail_template=self.__mail_template,
            extra_path=f"{self.__file_type}/{self.account_id}/users"
        )
        ep_create_upload_file.run()
