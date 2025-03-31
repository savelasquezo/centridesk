from shared.rabbitmq.infrastructure.sender import RabbitSender


class RabbitMQMailSender:

    def __init__(self, message=None):
        self.message = message

        self.__queue_name = 'platform_send_email'

    def send(self):
        rabbit_sender = RabbitSender(
            queue_name=self.__queue_name,
            message=self.message
        )
        rabbit_sender.send()
