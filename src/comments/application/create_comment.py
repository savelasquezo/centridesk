from time import sleep

from shared.exceptions.invalid_firebase_token import InvalidFirebaseToken
from shared.exceptions.not_found import NotFound
from src.users.application.delete_device_by_user import DeleteUserDeviceByUser


class CommentCreate:

    def __init__(self, account_id, comment, ticket, comments_obj, customers_obj, agents_obj, centribot_obj,
                 websocket_obj, bucket_obj, get_file_obj, firebase_obj, userstoken_obj, process_attachments_app,
                 is_file=False, converter_obj=None, files_obj=None):
        self.account_id = account_id
        self.comment = comment
        self.ticket = ticket
        self.comments_obj = comments_obj
        self.customers_obj = customers_obj
        self.agents_obj = agents_obj
        self.centribot_obj = centribot_obj
        self.websocket_obj = websocket_obj
        self.bucket_obj = bucket_obj
        self.get_file_obj = get_file_obj
        self.firebase_obj = firebase_obj
        self.userstoken_obj = userstoken_obj
        self.process_attachments_app = process_attachments_app
        self.is_file = is_file
        self.converter_obj = converter_obj
        self.files_obj = files_obj

    def create(self):
        # check author_id exists as customer or agent
        self.customers_obj.account_id = self.comments_obj.account_id = self.account_id
        self.customers_obj.customer_id = self.comment.author_id

        customer = self.customers_obj.get_by_id()
        if not customer:
            self.agents_obj.agent_id = self.comment.author_id

            if not self.agents_obj.get_by_id():
                raise NotFound('author ID')

            self.comment.is_agent = True

        # process attachments
        self.process_attachments_app.account_id = self.account_id
        self.process_attachments_app.attachments = self.comment.attachments
        self.process_attachments_app.get_file_obj = self.get_file_obj
        self.process_attachments_app.bucket_obj = self.bucket_obj
        self.process_attachments_app.converter_obj = self.converter_obj
        self.process_attachments_app.files_obj = self.files_obj
        self.process_attachments_app.ticket_id = self.ticket['id']
        self.comment.attachments = self.process_attachments_app.process_attachments()

        # create comment
        self.comments_obj.comment = self.comment
        self.comments_obj.create()

        if customer:
            self.customers_obj.update_last_comment_at(customer['id'], self.comment.timestamp)

        # send to centribot
        if self.comment.public and self.ticket['tags'] \
                and 'platform_centribot' in self.ticket['tags'] \
                and all(t not in self.ticket['tags'] for t in ['platform_centribot_solved', 'centribot_out_of_office']) \
                and self.comment.author_id != self.ticket['author_id'] \
                and self.ticket['centribot_project_id'] \
                and self.ticket['centribot_channel_id'] \
                and self.ticket['external_id']:
            self.centribot_obj.project_id = self.ticket['centribot_project_id']
            self.centribot_obj.channel_id = self.ticket['centribot_channel_id']
            self.centribot_obj.external_id = self.ticket['external_id']
            self.centribot_obj.ticket_id = self.comment.ticket_id
            self.centribot_obj.comment_id = self.comment.comment_id
            self.centribot_obj.message = self.comment.text if not self.is_file else ''
            self.centribot_obj.attachments = self.comment.attachments.data if self.comment.attachments else []
            self.centribot_obj.requester_id = self.comment.author_id
            self.centribot_obj.send_message()

        self.comments_obj.ticket_id = self.comment.ticket_id
        self.comments_obj.comment_id = self.comment.comment_id

        try:
            comment = self.comments_obj.get_by_id()
        except NotFound:
            sleep(1)
            comment = self.comments_obj.get_by_id()

        # websocket connection
        self.websocket_obj.account_id = self.account_id
        self.websocket_obj.ticket_id = self.comment.ticket_id
        self.websocket_obj.ticket_auto_id = self.ticket['auto_id']
        self.websocket_obj.ticket_subject = self.ticket['subject']
        self.websocket_obj.ticket_status = self.ticket['status']
        self.websocket_obj.ticket_status_id = self.ticket['status_id']
        self.websocket_obj.ticket_customer_id = self.ticket['author_id'] if not self.ticket['is_agent'] else None
        self.websocket_obj.comment_id = comment['id']
        self.websocket_obj.comment_author_id = comment['author_id']
        self.websocket_obj.comment_text = comment['text']
        self.websocket_obj.comment_text_json = comment['text_json']
        self.websocket_obj.comment_is_agent = comment['is_agent']
        self.websocket_obj.comment_public = comment['public']
        self.websocket_obj.comment_created_at = comment['created_at']
        self.websocket_obj.comment_attachments = comment['attachments']
        self.websocket_obj.send_new()

        # send notification to mobile
        if not self.comment.is_agent and self.ticket['assignee_id']:
            self.userstoken_obj.centribot_user_id = self.ticket['assignee_id']
            user_token = self.userstoken_obj.get()
            if user_token:
                mobile_ids = user_token['mobile_id'] or []

                for mobile_id in mobile_ids:
                    try:
                        self.firebase_obj.send_create_ticket_or_comment_notification(
                            token=mobile_id,
                            customer_id=self.comment.author_id,
                            customer_name=customer['name']
                        )
                    except InvalidFirebaseToken:
                        delete_device_app = DeleteUserDeviceByUser(
                            user_id=self.ticket['assignee_id'],
                            mobile_id=mobile_id,
                            userstoken_obj=self.userstoken_obj
                        )
                        delete_device_app.delete()

        return comment
