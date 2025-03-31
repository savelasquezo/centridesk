class RabbitMQCentrideskGenericsSender:

    def __init__(self, message=None):
        self.message = message
        self.__queue_name = 'centridesk_generics'

    def send(self):
        pass
