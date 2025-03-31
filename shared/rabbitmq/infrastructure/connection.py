import ssl

import pika

from shared.infrastructure.get_config import GetConfig


class RabbitConnection:

    def __init__(self, queue_name, message=None):
        self.rabbitmq = self._get_config()
        self.conn, self.channel = self._get_conn()
        self.queue_name = queue_name
        self.message = message

    @staticmethod
    def _get_config():
        return GetConfig().get_rmq()

    def _get_conn(self):
        try:
            __config = GetConfig()

            credentials = pika.PlainCredentials(self.rabbitmq.user, self.rabbitmq.password)
            parameters = pika.ConnectionParameters(self.rabbitmq.host, self.rabbitmq.port,
                                                   self.rabbitmq.vhost, credentials)

            if __config.is_kubernetes():
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
                parameters._ssl_options = pika.SSLOptions(context=ssl_context)

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

        except Exception as ex:
            raise Exception(f"Error getting rabbit connection: {ex}")

        return connection, channel

    def close(self):
        try:
            self.conn.close()
        except Exception as ex:
            raise Exception(f"Queue: {self.queue_name} \nError closing rabbit connection: {ex}")

    def publish(self):
        try:
            self.channel.queue_declare(self.queue_name, durable=True)
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=self.message,
                properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
            )

        except Exception as ex:
            raise Exception(f"Queue: {self.queue_name} \n Message: {self.message} \nError publishing message: {ex}")

    def delete_queue(self):
        try:
            self.channel.queue_delete(queue=self.queue_name)
        except Exception as ex:
            raise Exception(f"Queue: {self.queue_name} \nError deleting queue: {ex}")
