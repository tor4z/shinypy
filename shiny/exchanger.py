from .message import Message, Method


class Mapping:
    def __init__(self):
        self._in_map = {}
        self._out_map = {}
        self.inited = False

    def bind(self, in_port, out_port):
        # Double end binding
        if not self.inited:
            self._bind(self._in_map, in_port, out_port)
            self._bind(self._out_map, out_port, in_port)

    def _bind(self, map, key1, key2):
        if key1 in map:
            map[key1].add(key2)
        else:
            map[key1] = {key2}

    def get_outs(self, in_port):
        return self._in_map.get(in_port, set())

    def get_ins(self, out_port):
        return self._out_map.get(out_port, set())


class In:
    def __init__(self, msg, mapping, ws):
        self._out_port = None
        self._data = msg.data if msg else {}
        self.mapping = mapping
        self._ws = ws

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, in_port):
        self.mapping.bind(in_port, self._out_port)
        # if in_port not in self._data:
        #    data = await self._ws.query(in_port)
        #    self._data.update(data)
        return self._data[in_port]

    async def cache(self, in_ports):
        if in_ports:
            to_cache = []
            for in_port in in_ports:
                if in_port not in self._data.keys():
                    to_cache.append(in_port)

            data = await self._ws.query(to_cache)
            self._data.update(data)

    @property
    def in_ports(self):
        return self._data.keys()

    def instance(self, out_port):
        self._out_port = out_port
        return self


class Out:
    def __init__(self, iner):
        self._in = iner
        self.mapping = iner.mapping
        self._outs = {}
        self._data = {}

    def __setitem__(self, key, func):
        self._outs[key] = func

    def __getitem__(self, key):
        raise NotImplementedError

    def init_execute(self):
        self._execute(self._outs.keys())

    async def execute(self):
        out_ports = set()
        in_ports = set()

        for in_port in self._in.in_ports:
            out_ports.update(self.mapping.get_outs(in_port))

        for out_port in out_ports:
            in_ports.update(self.mapping.get_ins(out_port))

        await self._in.cache(in_ports)
        self._execute(out_ports)

    def _execute(self, outs):
        for out_port in outs:
            func = self._outs[out_port]
            iner = self._in.instance(out_port)
            self._data[out_port] = func(iner)

    @property
    def msg(self):
        msg = Message()
        msg.data = self._data
        msg.method = Method.SET
        return msg
