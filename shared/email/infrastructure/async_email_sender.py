from shared.async_queue.infrastructure.sender_mail import AsyncMailSender


class EmailSender:

    def __init__(self, email, template, language, params=None, attachments=None, subject=None) -> None:
        self.email = email
        self.template = template
        self.language = language
        self.params = params or {}
        self.attachments = attachments or []
        self.subject = subject

    def send(self):
        sender = AsyncMailSender(
            message={
                'email': self.email,
                'template': self.template,
                'lang': self.language,
                'params': self.params,
                'attachments': self.attachments,
                'subject': self.subject
            }
        )
        sender.send()
