from .wstream import string_to_json, json_to_string


class Mapping:
    def __init__(self):
        self._in_map = {}
        self._out_map = {}

    def bind(self, in_port, out_port):
        # Double end binding
        # TODO Fix multi-binding
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
        self._data = string_to_json(msg)
        self.mapping = mapping
        self._ws = ws

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, in_port):
        self.mapping.bind(in_port, self._out_port)
        if in_port in self._data:
            return self._data[in_port]
        else:
            # Get data from client
            # Cache data
            pass

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

    def __setitem__(self, key, func):
        self._outs[key] = func

    def __getitem__(self, key):
        raise NotImplementedError

    def _out_data(self):
        # TODO lazy I/O
        data = {}
        out_ports = set()
        for in_port in self._in.in_ports:
            out_ports.union(self.mapping.get_outs(in_port))

        for out_port in out_ports:
            func = self._outs[out_port]
            iner = self._in.instance(out_port)
            data[out_port] = func(iner)
        return data

    def __str__(self):
        return json_to_string(self._out_data())

    __repr__ = __str__
