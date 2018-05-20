import traceback


class Exchanger:
    def __init__(self):
        pass


class In:
    def __init__(self, exchanger):
        self._exchanger = exchanger

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key):
        pass


class Out:
    def __init__(self, exchanger):
        self._exchanger = exchanger

    def __setitem__(self, key, func):
        pass

    def __getitem__(self, key):
        pass