from json import loads

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.pagination.paginator import Paginator
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.aws_bucket.infrastructure.buckets import AwsBuckets
from shared.files.infrastructure.download_from_url import FileFromUrl
from shared.firebase.infrastructure.firebase_connector import FirebaseConnector
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.auth.infrastructure.users_token_orm import UsersTokenOrm
from src.centribot.infrasctructure.centribot_requests import CentribotRequests
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.comments.application.create_comment import CommentCreate
from src.comments.application.get_comments import GetComments
from src.comments.application.process_attachments_from_smooch import ProcessAttachmentsSmooch
from src.comments.domain.comment_in import CommentIn
from src.comments.infrastructure.comments_mysql import CommentsMysql
from src.comments.infrastructure.websocket import CommentsWebsocket
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.application.ticket_get import GetTicket
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class Comments(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        data = loads(request.body.decode('utf-8'))

        app = GetTicket(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            tickets_obj=TicketsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            status_dict={s['id']: s['name'] for s in StatusOrm().get_all()},
            priorities_dict={p['id']: p['name'] for p in PrioritiesOrm().get_all()},
            channels_dict={c['id']: c['name'] for c in ChannelsMysql().get_all()}
        )
        ticket = app.get()

        app = CommentCreate(
            account_id=kwargs['account_id'],
            comment=CommentIn(ticket_id=kwargs['ticket_id'], **data),
            ticket=ticket,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=FirebaseConnector(),
            userstoken_obj=UsersTokenOrm(),
            process_attachments_app=ProcessAttachmentsSmooch()
        )

        return app.create()

    @api_handler
    def get(self, request, **kwargs):
        paginator = Paginator(request.GET.get('page', None), request.GET.get('page_size', None), 'comments')

        app = GetComments(
            account_id=kwargs['account_id'],
            ticket_id=kwargs['ticket_id'],
            comments_obj=CommentsMysql(),
            tickets_obj=TicketsMysql(),
            sort=request.GET.get('sort', None),
            order=request.GET.get('order', None),
            page=paginator.page,
            page_size=paginator.page_size
        )

        paginator.results, paginator.total = app.get()

        return paginator.get_response()
