import socket
from os import path as os_path
from sys import path as sys_path
from centribal.packages.utils.get_config import GetConfig
from centribal.packages.utils.activemq.consumer import Reciever
from urllib3.connection import HTTPConnection, HTTPSConnection
sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from src.generics.infrastructure.ep_centridesk_generics import EntrypointGenerics

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 300),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 45)
    ]
)

HTTPSConnection.default_socket_options = (
    HTTPSConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 300),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 45)
    ]
)

if __name__ == '__main__':
    try:
        root_path = f"{os_path.dirname(os_path.abspath(__file__))}/.."
        GetConfig.load_config(root_path)
        logger = GetConfig.get_logger()
        queue_config = GetConfig.get_queue_config()
        receiver = Reciever(
            config=queue_config,
            queue='centridesk.generics',
            callback_class=EntrypointGenerics,
            logger=logger
        )
        logger.debug('Centridesk Generics ActiveMQ Reciever has been setted',
                     extra={
                        'queue': 'centridesk.generics', 
                        'config': str(queue_config)
                    })
        receiver.run()

    except Exception:
        logger.error(
            'Error initiating Centridesk Generics Consumer',
            exc_info=True,
            extra={
                'queue': 'centridesk.generics', 
                'config': str(queue_config)
            }
        )
