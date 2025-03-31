from shared.email.infrastructure.async_email_sender import EmailSender
from src.agents.infrastructure.agents_mysql import AgentsMysql


class MailSender:

    def __init__(self, requester_id=None, superadmin=None, template=None, params=None):
        self.requester_id = requester_id
        self.superadmin = superadmin
        self.template = template
        self.params = params

        self.__centribot_operations_id = '78a64c9b997144e28f08faba699882a4'

    def send(self):
        to_send = [{'email': self.superadmin['username'], 'lang': self.superadmin['lang']}]

        # if requester is not superadmin and not centribot_operations
        if self.requester_id not in [self.superadmin['user_id'], self.__centribot_operations_id]:
            agents_obj = AgentsMysql(agent_id=self.requester_id)
            user = agents_obj.get_by_id()
            if user:
                to_send.append({'email': user['email'], 'lang': user['lang']})

        # send email to superadmin and requester
        for user in to_send:
            sender = EmailSender(
                email=user['email'],
                template=self.template,
                language=user['lang'],
                params=self.params
            )
            sender.send()
