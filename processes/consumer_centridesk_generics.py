from os import path as os_path
from sys import path as sys_path

import socket

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from centribal.packages.logger.log_manager import init_loggers
from shared.infrastructure.get_config import GetConfig
from shared.rabbitmq.infrastructure.receiver import RabbitReceiver
from src.generics.infrastructure.ep_centridesk_generics import EntrypointGenerics
from urllib3.connection import HTTPConnection, HTTPSConnection

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
    configLog = GetConfig.load_config(sys_path)
    logger = init_loggers(**configLog.get_logs())
    try:
        r = RabbitReceiver('centridesk_generics', EntrypointGenerics)
        r.read()

    except Exception as ex:
        logger.error('Error initiating Centridesk Generics Consumer', exc_info=True)
