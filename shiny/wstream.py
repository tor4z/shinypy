from aiohttp.web import WSMsgType
import json


def json_to_string(data):
    return json.dumps(data)


def string_to_json(string):
    return json.loads(string)


class Wstream:
    def __init__(self, resp):
        self._ws = resp

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            msg, type = await self.receive_data()
            return msg, type
        except WstreamExp:
            raise StopAsyncIteration

    async def get(self, key):
        data = MessageParser.get(key)
        await self.send_data(data)
        data, type = await self.receive_data()
        return MessageParser.value(data)

    async def receive_data(self, *args, **kwargs):
        msg, type = await self.receive(*args, **kwargs)
        if type is MsgType.TEXT:
            data = string_to_json(msg.data)
            return data, msg.DICT

    async def receive(self, *args, **kwargs):
        msg = await self._ws.receive(*args, **kwargs)
        if msg.type in (MsgType.CLOSE,
                        MsgType.CLOSING,
                        MsgType.CLOSED):
            raise WstreamExp("WebSocket closed.")
        return msg.data, msg.type

    async def send_str(self, string):
        if not isinstance(string, str):
            raise TypeError("str required.")
        await self._ws.send_str(string)

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


class MsgType(WSMsgType):
    DICT = 0x103
    dict = DICT


class MessageParser:
    '''
    All message should be a json string.
    Get:
        query msg:
        {
            method: 'GET',
            data: {
                keys: ['key1', 'key2', 'key3', ...]
            }
        }
        responses msg:
        {
            status: status_code,
            reason: 'Error message',
            data: {
                key: value (single value or array of value)
            }
        }

    Set:
        set msg
        {
            method: 'SET',
            data: {}
        }
        responses msg:
        {
            status: status_code,
            reason: 'Error message'
        }

    Execute:
        {
            method: 'EXEC',
            data: {}
        }

        {
            status: status_code,
            reason: 'Error message',
            data: {}
        }
    '''
    @classmethod
    def get(cls, *keys):
        msg = {}
        msg['method'] = 'GET'
        msg['data'] = {'keys': list(keys)}
        return json_to_string(msg)

    def __init__(self, msg):
        if isinstance(msg, str):
            msg = string_to_json(msg)
        self.msg = msg

    @property
    def status_code(self):
        pass

    @property
    def reason(self):
        pass

    @property
    def data(self):
        pass

    def value(self, key=None):
        if key is None:
            pass
        else:
            pass


class WstreamExp(Exception):
    pass
