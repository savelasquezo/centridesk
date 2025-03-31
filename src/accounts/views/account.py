from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from src.accounts.application.delete_account import DeleteAccount
from src.accounts.application.get_account import GetAccount
from src.accounts.infrastructure.accounts_database_mysql import AccountsDatabaseMysql
from src.accounts.infrastructure.accounts_orm import AccountsOrm
from src.auth.infrastructure.my_token_orm import MyTokenOrm
from shared.exceptions.user_not_allowed import UserNotAllowed


class AccountView(APIView):
    permission_classes = (IsAuthenticated,)

    @api_handler
    def get(self, request, **kwargs):
        app = GetAccount(
            account_id=kwargs['account_id'],
            accounts_obj=AccountsOrm(),
            token_obj=MyTokenOrm())
        output = app.get()

        return output

    @api_handler
    def delete(self, request, **kwargs):
        if request.user.username != 'centribot_operations':
            raise UserNotAllowed()

        app = DeleteAccount(
            account_id=kwargs['account_id'],
            accounts_obj=AccountsOrm(),
            accounts_db_obj=AccountsDatabaseMysql()
        )
        app.delete()

        return {'message': 'ok'}
