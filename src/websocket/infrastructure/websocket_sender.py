from centridesk.settings import BASE_DIR
from centribal.packages.utils.get_config import GetConfig
from centribal.packages.logger.log_manager import init_loggers
from src.websocket.infrastructure.get_or_create_event_loop import get_or_create_event_loop
from src.websocket.infrastructure.websocket_connection import WebsocketConnection


class WebsocketSender:

    def __init__(self, channel=None, body=None):
        self.channel = channel
        self.body = body

    def send(self):
        config = GetConfig.load_config(BASE_DIR)
        logger = init_loggers(**config.get_logs())
        try:
            __ws = WebsocketConnection(channel=self.channel)
            event_loop = get_or_create_event_loop()
            event_loop.run_until_complete(__ws.send(self.body))

        except Exception as ex:
            logger.error('Warning: Websocket connection lost',
                    extra={
                        'Body': self.body
                        },
                    exc_info=True)
