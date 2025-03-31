from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

from src.accounts.infrastructure.accounts_mysql import AccountsMysql
from src.accounts.infrastructure.accounts_orm import AccountsOrm
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.auth.infrastructure.users_token_orm import UsersTokenOrm


class PermissionsStaticUserToken(permissions.BasePermission):
    def has_permission(self, request, view):
        header_authentication = request.headers.get('Authentication', None)
        if header_authentication:
            token = header_authentication.split(' ')[1]
            if token:
                # check account exists
                user_token = UsersTokenOrm(key=token)
                exist_user = user_token.get_by_key()

                if exist_user:
                    # Check active user
                    agents = AgentsMysql(agent_id=exist_user['centribot_user_id'])
                    agent = agents.get_by_id()

                    if not agent or not agent['active']:
                        raise AuthenticationFailed

                    # Check active account
                    agents.agent_id = agent['id']
                    account = agents.get_account()

                    if not account:
                        raise AuthenticationFailed

                    accounts = AccountsOrm(account_id=account['account_id'])
                    account_exists = accounts.check_exists()

                    if not account_exists:
                        raise AuthenticationFailed

                    account_centribot_db = AccountsMysql(account_id=account['account_id'])
                    account_active = account_centribot_db.check_active()
                    if not account_active['active']:
                        raise AuthenticationFailed

                    request.user.unique_id = account['account_id']

                    return True
                else:
                    raise AuthenticationFailed
