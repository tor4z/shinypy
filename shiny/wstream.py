import json


class Wstream:
    _QUERY = "query"
    _RESULT = "result"

    def __init__(self, ws):
        self._ws = ws

    @staticmethod
    def str_to_dict(self, string):
        return json.loads(string)

    @staticmethod
    def dict_to_str(self, dictionary):
        return json.dumps(dictionary)

    async def send_str(self, data):
        await self._ws.send_str(data)

    async def recv_str(self):
        data = await self._ws.send_str()
        return data

    async def send_dict(self, dictionary):
        string = self.dict_to_str(dictionary)
        await self.send_str(string)

    async def recv_dict(self):
        data = await self.recv_str()
        return self.str_to_dict(data)

    async def get(self, key):
        data = {self._QUERY: key}
        await self.send_dict(data)
        result = await self.recv_dict()
        return result[self._RESULT]

    async def close(self):
        await self._ws.close()
