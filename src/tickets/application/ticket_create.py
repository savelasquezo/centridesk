from shared.exceptions.invalid_firebase_token import InvalidFirebaseToken
from shared.exceptions.not_found import NotFound
from src.comments.domain.comment_in import CommentIn
from src.tickets.application.ticket_get import GetTicket
from src.users.application.delete_device_by_user import DeleteUserDeviceByUser


class TicketCreate:

    def __init__(self, account_id, ticket, tickets_obj, comments_obj, customers_obj, priority_obj, status_obj,
                 channels_obj, agents_obj, websocket_obj, firebase_obj, userstoken_obj):
        self.account_id = account_id
        self.ticket = ticket
        self.tickets_obj = tickets_obj
        self.comments_obj = comments_obj
        self.customers_obj = customers_obj
        self.priority_obj = priority_obj
        self.status_obj = status_obj
        self.channels_obj = channels_obj
        self.agents_obj = agents_obj
        self.websocket_obj = websocket_obj
        self.firebase_obj = firebase_obj
        self.userstoken_obj = userstoken_obj

    def create(self):
        __comment_is_agent = False
        # check customer exists if it's not null
        self.customers_obj.account_id = self.account_id
        self.customers_obj.customer_id = self.ticket.author_id
        customer = self.customers_obj.get_by_id()
        if self.ticket.author_id:
            if not customer:
                raise Exception('customer not found')
            else:
                # Auto-assign agent if agent_id is filled and is valid
                if customer['agent_id'] and not self.ticket.assignee_id:
                    self.agents_obj.agent_id = customer['agent_id']
                    agent = self.agents_obj.get_by_id()
                    if agent and agent['active']:
                        self.ticket.assignee_id = customer['agent_id']

            if self.ticket.requester_id and self.ticket.requester_id != self.ticket.author_id:
                __comment_is_agent = True

        else:
            if self.ticket.requester_id:
                self.ticket.author_id = self.ticket.requester_id
                self.ticket.is_agent = __comment_is_agent = True

        # priority
        if self.ticket.priority and not self.ticket.priority_id:
            self.priority_obj.name = self.ticket.priority
            priority = self.priority_obj.get_by_name()
            self.ticket.priority_id = priority['id']

        # status
        if self.ticket.status and not self.ticket.status_id:
            self.status_obj.name = self.ticket.status
            status = self.status_obj.get_by_name()
            self.ticket.status_id = status['id']

        # channel
        if self.ticket.channel_id:
            self.channels_obj.channel_id = self.ticket.channel_id
            channel = self.channels_obj.get_by_id()

            if not channel:
                raise NotFound('channel')

        if self.ticket.platform and not self.ticket.channel_id:
            self.channels_obj.platform = self.ticket.platform
            channel = self.channels_obj.get_by_platform()

            if not channel:
                raise NotFound('platform')

            self.ticket.channel_id = channel['id']

        # assignee_id
        if self.ticket.assignee_id:
            self.agents_obj.agent_id = self.ticket.assignee_id
            assignee_role = self.agents_obj.get_rol_by_user()
            if not assignee_role or not assignee_role['desk']:
                raise NotFound('assignee')

        # create ticket
        self.tickets_obj.account_id = self.account_id
        self.tickets_obj.ticket = self.ticket
        self.tickets_obj.create()

        # create first comment / description
        __comment = CommentIn(
            text=self.ticket.description,
            text_json=self.ticket.description_json,
            author_id=self.ticket.requester_id or self.ticket.author_id,
            is_agent=__comment_is_agent,
            public=self.ticket.public,
            ticket_id=self.ticket.ticket_id
        )
        self.comments_obj.comment = __comment
        self.comments_obj.account_id = self.account_id
        self.comments_obj.create()

        if customer and __comment_is_agent is False:
            self.customers_obj.update_last_comment_at(customer['id'], __comment.timestamp)

        # send notification to mobile
        if self.ticket.assignee_id:
            self.userstoken_obj.centribot_user_id = self.ticket.assignee_id
            user_token = self.userstoken_obj.get()
            if user_token:
                mobile_ids = user_token['mobile_id'] or []

                for mobile_id in mobile_ids:
                    try:
                        self.firebase_obj.send_create_ticket_or_comment_notification(
                            token=mobile_id,
                            customer_id=self.ticket.author_id,
                            customer_name=customer['name']
                        )
                    except InvalidFirebaseToken:
                        delete_device_app = DeleteUserDeviceByUser(
                            user_id=self.ticket.assignee_id,
                            mobile_id=mobile_id,
                            userstoken_obj=self.userstoken_obj
                        )
                        delete_device_app.delete()

        # todo rollback

        getter = GetTicket(
            account_id=self.account_id,
            ticket_id=self.ticket.ticket_id,
            tickets_obj=self.tickets_obj,
            customers_obj=self.customers_obj,
            agents_obj=self.agents_obj
        )
        ticket = getter.get()

        # websocket connection
        self.websocket_obj.account_id = self.account_id
        self.websocket_obj.ticket_id = self.ticket.ticket_id
        self.websocket_obj.auto_id = ticket['auto_id']
        self.websocket_obj.author_id = ticket['author_id']
        self.websocket_obj.subject = ticket['subject']
        self.websocket_obj.status = self.ticket.status
        self.websocket_obj.status_id = self.ticket.status_id
        self.websocket_obj.comment = __comment
        self.websocket_obj.customer_id = ticket['author_id'] if not self.ticket.is_agent else None
        self.websocket_obj.created_at = ticket['created_at']
        self.websocket_obj.send_new()

        return ticket
