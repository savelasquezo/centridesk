from shared.rabbitmq.infrastructure.sender_mail import RabbitMQMailSender


class RabbitMqEmailSender:

    def __init__(self, email, template, language, params=None, attachments=None, subject=None) -> None:
        self.email = email
        self.template = template
        self.language = language
        self.params = params or {}
        self.attachments = attachments or []
        self.subject = subject

    def send(self):
        rmq = RabbitMQMailSender(
            message={
                'email': self.email,
                'template': self.template,
                'lang': self.language,
                'params': self.params,
                'attachments': self.attachments,
                'subject': self.subject
            }
        )
        rmq.send()
