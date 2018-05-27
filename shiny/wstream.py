from enum import IntEnum
from .message import Message
from .util import json_to_string, string_to_json


class WSMsgType(IntEnum):
    # websocket spec types
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    PING = 0x9
    PONG = 0xa
    CLOSE = 0x8

    # aiohttp specific types
    CLOSING = 0x100
    CLOSED = 0x101
    ERROR = 0x102

    # shiny specific types
    DICT = 0x103
    MSG = 0x104

    text = TEXT
    binary = BINARY
    ping = PING
    pong = PONG
    close = CLOSE
    closing = CLOSING
    closed = CLOSED
    error = ERROR
    dict = DICT
    msg = MSG


class WStream:
    def __init__(self, resp):
        self._ws = resp

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            msg, type = await self.receive_msg()
            return msg, type
        except WStreamExp:
            raise StopAsyncIteration

    async def query(self, keys):
        msg = Message()
        msg.query(keys)
        await self.send_msg(msg)
        result, _ = await self.receive_msg()
        return result.data

    async def receive_msg(self, *args, **kwargs):
        string, type = await self.receive(*args, **kwargs)
        if type is WSMsgType.TEXT:
            msg = Message(string)
            return msg, msg.MSG

    async def receive_data(self, *args, **kwargs):
        msg, type = await self.receive(*args, **kwargs)
        if type is WSMsgType.TEXT:
            data = string_to_json(msg.data)
            return data, msg.DICT

    async def receive(self, *args, **kwargs):
        msg = await self._ws.receive(*args, **kwargs)
        if msg.type in (WSMsgType.CLOSE,
                        WSMsgType.CLOSING,
                        WSMsgType.CLOSED):
            raise WStreamExp("WebSocket closed.")
        return msg.data, msg.type

    async def send_str(self, string):
        if not isinstance(string, str):
            raise TypeError("str required.")
        await self._ws.send_str(string)

    async def send_msg(self, msg):
        if not isinstance(msg, Message):
            raise TypeError("Message required.")
        await self._ws.send_str(str(msg))

    async def send_data(self, data):
        if not isinstance(data, dict):
            raise TypeError("dict required.")
        string = json_to_string(data)
        await self.send_str(string)

    async def close(self):
        await self._ws.close()

    @property
    def raw(self):
        return self._ws


class WStreamExp(Exception):
    pass
