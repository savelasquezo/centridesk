from shared.infrastructure.b64 import encode_obj
from shared.rabbitmq.infrastructure.connection import RabbitConnection


class RabbitSender:
    def __init__(self, message=None, queue_name=None):
        self.message = message
        self.queue_name = queue_name

    def send(self):
        try:
            conn = RabbitConnection(self.queue_name, encode_obj(self.message))
            conn.publish()
            conn.close()

        except Exception as ex:
            raise Exception(f"Error Publishing Rabbit Message: {self.message} \nError: {ex}")
