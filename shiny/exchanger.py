class Exchanger:
    def __init__(self, wstream):
        self._wstream = wstream
        self._mapping = {}
        self._tasks = []
    
    def register(self, out_port):
        self._mapping[out_port] = []

    def subscribe(self, out_port, in_port):
        self._mapping[out_port].append(in_port)

    async def get(self, key):
        return await self._wstream.get(key)

    async def consume(self):
        task, out_port = self._tasks.pop()
        result = task()
        data = {out_port: result}
        await self._wstream.send_dict(data)

    def start(self):
        pass


class In:
    def __init__(self, exchanger):
        self._exchanger = exchanger
        self._out_port = None

    def register(self, out_port):
        self._exchanger.register(out_port)
        self._out_port = out_port

    def __setitem__(self, key, value):
        raise NotImplementedError

    async def __getitem__(self, key):
        self._exchanger.subscribe(self._out_port ,key)
        return await self._exchanger.get(key)


class Out:
    def __init__(self, wstream):
        self._wstream = wstream

    async def __setitem__(self, key, func):
        await self._wstream.send_dict({key: func()})

    def __getitem__(self, key):
        raise NotImplementedError
