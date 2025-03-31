from json import dumps

import websockets

from shared.infrastructure.get_config import GetConfig


class WebsocketConnection:

    def __init__(self, channel):
        self.__config = GetConfig().get('platform.websockets')
        self.channel = channel

    @staticmethod
    async def __send(ws, message):
        await ws.send(dumps(message))

    async def __connect(self, ws):
        await self.__send(ws, {"type": "centridesk", "channel": self.channel})

    async def send(self, message):
        try:
            async with websockets.connect(self.__config.url) as ws:
                await self.__connect(ws)
                await self.__send(ws, message)

        except Exception as ex:
            raise Exception(f'Websocket Send. \nMessage: {message} \nError: {ex}')
