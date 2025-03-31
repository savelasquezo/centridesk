from shared.infrastructure.b64 import decode_obj
from shared.rabbitmq.infrastructure.connection import RabbitConnection


class RabbitReceiver:
    def __init__(self, queue_name, callback_class, params=None):
        self.queue_name = queue_name
        self.callback_class = callback_class
        self.params = params

    def read(self):
        rabbit = RabbitConnection(self.queue_name)
        rabbit.channel.queue_declare(self.queue_name, durable=True)
        rabbit.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        rabbit.channel.start_consuming()

    def callback(self, ch, method, props, body):
        try:
            message = decode_obj(body)

            app = self.callback_class(message, self.params) if self.params else self.callback_class(message)
            app.run()

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as ex:
            raise Exception(f"Error Callback: {ex}")
