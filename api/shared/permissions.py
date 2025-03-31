from shared.exceptions.user_not_allowed import UserNotAllowed
from src.accounts.infrastructure.accounts_orm import AccountsOrm
from src.agents.infrastructure.agents_mysql import AgentsMysql


def check_by_account(account_id, requester):
    if account_id and requester:
        platform_user = getattr(requester, 'catuser', None)

        # via jwt
        if platform_user:
            # check account exists
            accounts = AccountsOrm(account_id=account_id)
            accounts.get()

            if requester.username != 'centribot_operations':
                # get account by user_id
                agent = AgentsMysql(platform_user.unique_id)
                agent_info = agent.get_account()

                if not agent_info:
                    raise Exception('Agent without account')

                if agent_info['account_id'] != account_id:
                    raise UserNotAllowed

        else:
            # via custom token
            user_id = getattr(requester, 'unique_id')
            if user_id and account_id != user_id:
                raise UserNotAllowed
