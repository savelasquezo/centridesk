class CentribotRequest:

    def __init__(self, project_id=None, channel_id=None, external_id=None, ticket_id=None, comment_id=None,
                 message=None):
        self.project_id = project_id
        self.channel_id = channel_id
        self.external_id = external_id
        self.ticket_id = ticket_id
        self.comment_id = comment_id
        self.message = message

    def send_message(self):
        pass
