from pandas import DataFrame
from shared.infrastructure.b64 import decode_obj, decode_text

from shared.infrastructure.timestamps import get_timestamp
from src.accounts.infrastructure.accounts_mysql import AccountsMysql
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.comments.infrastructure.comments_mysql import CommentsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.generics.infrastructure.ep_create_upload_file import EntrypointCreateUploadFile
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class EntrypointDownloadUseReport:
    def __init__(self, account_id, info, requester_id):
        self.account_id = account_id
        self.from_filter = info['from']
        self.to_filter = info['to']
        self.info = info
        self.requester_id = requester_id
        self.__mail_template = 'desk_download_use_report'
        self.__send_email = True
        self.__file_name = f'desk_{self.account_id}_{get_timestamp()}_{self.from_filter}-{self.to_filter}_use_report.xlsx'
        self.__file_type = 'centridesk'
        self.__columns = ['name', 'email', 'phone', 'company', 'delegation', 'external_id', 'gdpr', 'gdpr_updated_at',
                          'agent_id', 'created_at']
        
    def run(self):
        account_obj = AccountsMysql(account_id=self.account_id)
        superadmin = account_obj.get_superadmin()
        ticket_obj = TicketsMysql(account_id=self.account_id)
        tickets = ticket_obj.list_tickets(self.from_filter, self.to_filter)
        
        if len(tickets) > 0:
            tickets_df = DataFrame(tickets)

            # list customers and combine author_id with name
            customer_obj = CustomersMysql(account_id=self.account_id)
            customers = customer_obj.list_customers(tuple(set(tickets_df['author_id'])))
            customers_by_id = {c['unique_id']: c for c in customers}

            tickets_df['company'] = tickets_df.apply(
                lambda row: customers_by_id.get(row.author_id, {}).get(' company'), axis=1)
            tickets_df['delegation'] = tickets_df.apply(
                lambda row: customers_by_id.get(row.author_id, {}).get('delegation'), axis=1)
            tickets_df['external_id'] = tickets_df.apply(
                lambda row: customers_by_id.get(row.author_id, {}).get('external_id'), axis=1)
                        
            tickets_df['company'] = tickets_df['company'].apply(decode_obj)
            tickets_df['delegation'] = tickets_df['delegation'].apply(decode_obj)
            tickets_df['external_id'] = tickets_df['external_id'].apply(decode_obj)

            # list agents and combine author_id with name
            agent_obj = AgentsMysql(account_id=self.account_id)
            agents = agent_obj.list_agents()
            agents_by_id = {a['unique_id']: a['first_name'] + ' ' + a['last_name'] for a in agents}

            tickets_df['agent_id'] = tickets_df.apply(lambda row: agents_by_id.get(row.assignee_id), axis=1)
            tickets_df.rename(columns={'created_at': 'Date'}, inplace=True)
            tickets_df.set_index('Date', inplace=True)

            # comments by agent and day
            comments = CommentsMysql(account_id=self.account_id)
            agents_comments = comments.list_comments(self.from_filter, self.to_filter)
            comments_df = DataFrame(agents_comments)
            comments_by_date = comments_df.groupby('created_at')

            results = {}
            for name, group in comments_by_date:
                group_by_agent = group.groupby('author_id').size()
                results[name] = group_by_agent.to_dict()
            
            r = DataFrame(results.values(), index=results.keys())
            for x in agents_by_id:
                r.rename(columns={x: 'agent_id'}, inplace=True)
            r.index.name = 'Date'

            data = {
                'tickets': tickets_df[['agent_id', 'company', 'delegation', 'external_id']],
                'comments': r 
            }
            
        else:
            data = {
                'tickets': DataFrame({'No tickets found': ['No se encontraron tickets']})
            }

        ep_create_upload_file = EntrypointCreateUploadFile(
            dataframe= data,
            file_name= self.__file_name,
            file_type=self.__file_type,
            superadmin=superadmin,
            requester_id=self.requester_id,
            send_email=self.__send_email,
            mail_template=self.__mail_template,
            extra_path=f"{self.__file_type}/{self.account_id}/use_report"
        )
        ep_create_upload_file.run()

