class RabbitSender:

    def __init__(self, message=None, queue_name=None):
        self.message = message
        self.queue_name = queue_name

    def send(self):
        pass
