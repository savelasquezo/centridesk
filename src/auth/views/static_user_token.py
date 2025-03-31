from json import loads

from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from shared.exceptions.unauthorized import Unauthorized
from shared.infrastructure.b64 import decode_obj
from src.accounts.infrastructure.accounts_mysql import AccountsMysql
from src.accounts.infrastructure.accounts_orm import AccountsOrm
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.auth.domain.static_user_token_in import StaticUserTokenIn
from src.auth.infrastructure.my_user_authentication import MyUserAuthentication
from src.auth.infrastructure.users_token_orm import UsersTokenOrm


class StaticUserToken(APIView):

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        info = StaticUserTokenIn(
            username=data.get('username', None),
            password=data.get('password', None)
        )

        # Check user and password
        auth_user = MyUserAuthentication(username=info.username, password=info.password)
        auth_user.check_user_password()

        agents = AgentsMysql()
        agent = agents.get_by_username(info.username)

        # Check active agent
        if not agent or not agent['active']:
            raise Unauthorized('No active account found with the given credentials')

        # Check active account
        agents.agent_id = agent['id']
        account_id = agents.get_account()

        if not account_id:
            raise Unauthorized('No active account found with the given credentials')

        accounts = AccountsOrm(account_id=account_id['account_id'])
        account_exists = accounts.check_exists()

        if not account_exists:
            raise Unauthorized('No active account found with the given credentials')

        account_centribot_db = AccountsMysql(account_id=account_id['account_id'])
        account_active = account_centribot_db.check_active()
        if not account_active['active']:
            raise Unauthorized('No active account found with the given credentials')

        users_token_repo = UsersTokenOrm(centribot_user_id=agent['id'])
        access_created = users_token_repo.get()

        if not access_created:
            users_token_repo.created_at = info.timestamp_at
            access_created = users_token_repo.create()

        return {
            'access': access_created['key'],
            'account_id': account_id['account_id'],
            'agent': {
                'id': agent['id'],
                'name': agent['name'],
                'desk': agent['desk']
            },
        }
