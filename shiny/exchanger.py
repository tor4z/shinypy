from .wstream import string_to_json, json_to_string


class Mapping:
    def __init__(self):
        # TODO double end binding
        self._inited = []
        self._mapping = {}

    def set(self, in_port, out_port):
        if out_port in self._inited:
            return
        else:
            self._inited.append(out_port)

        if in_port in self._mapping:
            self._mapping[in_port].add(out_port)
        else:
            self._mapping[in_port] = {out_port}

    def get_outs(self, in_port):
        return self._mapping[in_port]


class In:
    def __init__(self, msg, mapping, ws):
        self._out_port = None
        self._data = string_to_json(msg)
        self.mapping = mapping
        self._ws = ws

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, in_port):
        self.mapping.set(in_port, self._out_port)
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
