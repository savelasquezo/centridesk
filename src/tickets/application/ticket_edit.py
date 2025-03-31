from shared.exceptions.invalid_firebase_token import InvalidFirebaseToken
from shared.exceptions.not_found import NotFound
from src.users.application.delete_device_by_user import DeleteUserDeviceByUser


class EditTicket:

    def __init__(self, account_id, ticket_id, ticket, ticket_bkup, tickets_obj, agents_obj, customers_obj,
                 centribot_obj, status_dict, priorities_dict, websocket_obj, firebase_obj, userstoken_obj):
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.ticket = ticket
        self.ticket_bkup = ticket_bkup
        self.tickets_obj = tickets_obj
        self.agents_obj = agents_obj
        self.customers_obj = customers_obj
        self.centribot_obj = centribot_obj
        self.status_dict = status_dict
        self.priorities_dict = priorities_dict
        self.websocket_obj = websocket_obj
        self.firebase_obj = firebase_obj
        self.userstoken_obj = userstoken_obj

    def edit(self):
        if self.ticket.assignee_id:
            self.agents_obj.agent_id = self.ticket.assignee_id
            agent = self.agents_obj.get_by_id()

            if not agent or not agent['active']:
                raise NotFound('assignee')

            assignee_role = self.agents_obj.get_rol_by_user()

            if not assignee_role or not assignee_role['desk']:
                raise NotFound('assignee')

            # send notification to mobile
            if self.ticket.assignee_id != self.ticket_bkup['assignee_id']:
                self.customers_obj.customer_id = self.ticket_bkup['author_id']
                customer = self.customers_obj.get_by_id()
                if customer:
                    self.userstoken_obj.centribot_user_id = self.ticket.assignee_id
                    user_token = self.userstoken_obj.get()
                    if user_token:
                        mobile_ids = user_token['mobile_id'] or []

                        for mobile_id in mobile_ids:
                            try:
                                self.firebase_obj.send_assignee_ticket_notification(
                                    token=mobile_id,
                                    customer_id=self.ticket_bkup['author_id'],
                                    customer_name=customer['name']
                                )
                            except InvalidFirebaseToken:
                                delete_device_app = DeleteUserDeviceByUser(
                                    user_id=self.ticket.assignee_id,
                                    mobile_id=mobile_id,
                                    userstoken_obj=self.userstoken_obj
                                )
                                delete_device_app.delete()

        if self.ticket_bkup['tags'] and 'platform_centribot' in self.ticket_bkup['tags'] \
                and all(
            t not in self.ticket_bkup['tags'] for t in ['platform_centribot_solved', 'centribot_out_of_office']) \
                and self.ticket_bkup['centribot_project_id'] \
                and self.ticket_bkup['centribot_channel_id'] \
                and self.ticket_bkup['external_id'] and self.ticket_bkup['status_id'] != self.ticket.status_id \
                and self.ticket.status_id == 5:  # solved

            self.centribot_obj.project_id = self.ticket_bkup['centribot_project_id']
            self.centribot_obj.channel_id = self.ticket_bkup['centribot_channel_id']
            self.centribot_obj.external_id = self.ticket_bkup['external_id']
            self.centribot_obj.ticket_id = self.ticket_id
            self.centribot_obj.update_solved_status()

            self.ticket.tags.append('platform_centribot_solved')

        self.tickets_obj.ticket_id = self.ticket_id
        self.tickets_obj.account_id = self.account_id
        self.tickets_obj.ticket = self.ticket
        self.tickets_obj.update()

        # todo rollback

        # websocket connection
        self.websocket_obj.account_id = self.account_id
        self.websocket_obj.ticket_id = self.ticket.ticket_id
        self.websocket_obj.auto_id = self.ticket_bkup['auto_id']
        self.websocket_obj.assignee_id = self.ticket.assignee_id
        self.websocket_obj.customer_id = self.ticket_bkup['author_id'] if not self.ticket_bkup['is_agent'] else None
        self.websocket_obj.send_updated()
