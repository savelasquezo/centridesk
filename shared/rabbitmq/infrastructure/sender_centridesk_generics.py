from shared.rabbitmq.infrastructure.sender import RabbitSender


class RabbitMQCentrideskGenericsSender:

    def __init__(self, message=None):
        self.message = message

        self.__queue_name = 'centridesk_generics'

    def send(self):
        rabbit_sender = RabbitSender(
            queue_name=self.__queue_name,
            message=self.message
        )
        rabbit_sender.send()
