from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from src.accounts.application.setup_account import SetUpAccount
from src.accounts.infrastructure.accounts_database_mysql import AccountsDatabaseMysql
from src.accounts.infrastructure.accounts_orm import AccountsOrm
from src.auth.infrastructure.my_token_orm import MyTokenOrm
from shared.exceptions.user_not_allowed import UserNotAllowed


class AccountsSetUpView(APIView):
    permission_classes = (IsAuthenticated,)

    @api_handler
    def post(self, request):
        if request.user.username != 'centribot_operations':
            raise UserNotAllowed()

        data = loads(request.body.decode('utf-8'))

        app = SetUpAccount(
            account_id=data['account_id'],
            accounts_obj=AccountsOrm(),
            setup_obj=AccountsDatabaseMysql(),
            token_obj=MyTokenOrm()
        )

        return app.set_up()
