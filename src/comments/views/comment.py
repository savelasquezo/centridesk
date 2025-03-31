from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.comments.application.get_comment import GetComment
from src.comments.infrastructure.comments_mysql import CommentsMysql


class Comment(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetComment(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            comment_id=kwargs['comment_id'],
            comments_obj=CommentsMysql()
        )
        return app.get()
