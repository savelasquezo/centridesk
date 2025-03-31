import re

from requests_toolbelt.multipart import decoder
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from shared.aws_bucket.infrastructure.buckets import AwsBuckets
from shared.files.infrastructure.audio_converter import AudioConverter
from shared.files.infrastructure.download_from_url import FileFromUrl
from shared.files.infrastructure.files import Files
from shared.files.infrastructure.video_converter import VideoConverter
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.centribot.infrasctructure.centribot_requests import CentribotRequests
from src.channels.infrastructure.channels_mysql import ChannelsMysql
from src.comments.application.create_comment import CommentCreate
from src.comments.application.process_attachments_from_desk import ProcessAttachmentsDesk
from src.comments.domain.comment_in_desk import CommentInDesk
from src.comments.infrastructure.comments_mysql import CommentsMysql
from src.comments.infrastructure.websocket import CommentsWebsocket
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.application.ticket_get import GetTicket
from src.tickets.infrastructure.priorities_orm import PrioritiesOrm
from src.tickets.infrastructure.status_orm import StatusOrm
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class Attachments(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def post(self, request, **kwargs):
        content_type = request.headers['Content-Type']
        res = decoder.MultipartDecoder(request.body, content_type)

        file_name = None
        file_type = None
        file_media_type = None
        encoded_file_content = None
        file_size = None
        author_id = None

        for part in res.parts:
            disposition = part.headers[b'Content-Disposition'].decode()
            if 'name="file"' in disposition:
                encoded_file_content = part.content
                file_media_type = part.headers[b'Content-Type'].decode()
                file_type = file_media_type.split('/')[0]
                match = re.search(r'filename=\"([\w\W]*\.\w*)\"', disposition)
                if match:
                    file_name = match.group(1)
            elif 'name="mediasize"' in disposition:
                file_size = part.content.decode()
            elif 'name="author_id"' in disposition:
                author_id = part.content.decode()

        attachments = [
            {
                'filename': file_name,
                'type': file_type if file_type == 'image' else 'file',
                'mediatype': file_media_type,
                'content': encoded_file_content,
                'mediasize': file_size
            }
        ]

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

        comment = CommentInDesk(
            text=file_name if file_type in ['text', 'application'] else '',
            ticket_id=kwargs['ticket_id'],
            author_id=author_id,
            attachments=attachments
        )

        converter_dispatcher = {
            'video': VideoConverter,
            'audio': AudioConverter
        }

        converter_obj = converter_dispatcher.get(comment.attachments.data[0]['filetype'])

        app = CommentCreate(
            account_id=kwargs['account_id'],
            comment=comment,
            ticket=ticket,
            comments_obj=CommentsMysql(),
            customers_obj=CustomersMysql(),
            agents_obj=AgentsMysql(),
            centribot_obj=CentribotRequests(),
            websocket_obj=CommentsWebsocket(),
            bucket_obj=AwsBuckets(file_type='centridesk'),
            get_file_obj=FileFromUrl(),
            firebase_obj=None,
            userstoken_obj=None,
            process_attachments_app=ProcessAttachmentsDesk(),
            is_file=True,
            converter_obj=converter_obj() if converter_obj else None,
            files_obj=Files(),
        )

        return app.create()
