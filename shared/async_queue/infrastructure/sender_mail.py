from os import path as os_path
from centribal.packages.utils.activemq.producer import Sender
from centribal.packages.utils.b64 import encode_obj
from centribal.packages.utils.get_config import GetConfig


class AsyncMailSender:

    def __init__(self, message: dict=None):
        self.message = message
        root_path = f"{os_path.dirname(os_path.abspath(__file__))}/../../../"
        GetConfig.load_config(root_path)
        self.logger = GetConfig.get_logger()
        self.queue_config = GetConfig.get_queue_config()

        self.__queue_name = 'platform.send_email'

    def send(self):
        try:
            sender = Sender(
                config=self.queue_config,
                queue=self.__queue_name,
                logger=self.logger
            )
            sender.message = encode_obj(self.message)
            sender.run()
            self.logger.debug(
                'Async Mail has processed a new message',
                extra={
                    'queue': self.__queue_name, 
                    'config': str(self.queue_config),
                    'message': self.message
                }
            )

        except Exception:          
            self.logger.error(
                'Error Publishing Mail Async Message', 
                extra={
                    'queue': self.__queue_name, 
                    'config': str(self.queue_config),
                    'message': self.message
                },
                exc_info=True
            )
