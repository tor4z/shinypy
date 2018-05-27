from enum import IntEnum
from .util import json_to_string, string_to_json


class Method:
    GET = 'GET'
    SET = 'SET'
    EXEC = 'EXEC'


class Status(IntEnum):
    SUCCESS = 0
    ERROR = 1

    success = SUCCESS
    error = ERROR


class Message:
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
            reason: 'Error message',
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
    METHOD = 'method'
    DATA = 'data'
    KEYS = 'keys'
    REASON = 'reason'
    STATUS = 'status'

    def __init__(self, msg=None):
        if msg is not None and isinstance(msg, str):
            msg = string_to_json(msg)
        self.msg = msg or {}

    def query(self, keys):
        if not isinstance(keys, list):
            keys = [keys]
        self.method = Method.GET
        self.data = {self.KEYS: keys}

    @property
    def status(self):
        return self.msg.get(self.STATUS)

    @status.setter
    def status(self, status):
        self.msg[self.STATUS] = status

    @property
    def reason(self):
        return self.msg.get(self.REASON)

    @reason.setter
    def reason(self, reason):
        self.msg[self.REASON] = reason

    @property
    def method(self):
        return self.msg.get(self.METHOD)

    @method.setter
    def method(self, method):
        self.msg[self.METHOD] = method

    @property
    def keys(self):
        if self.method == Method.GET:
            return self.data.get(self.KEYS)
        else:
            return self.data.keys()

    @property
    def data(self):
        return self.msg.get(self.DATA)

    @data.setter
    def data(self, data):
        self.msg[self.DATA] = data

    def __setitem__(self, key, value):
        if self.msg.get(self.DATA) is None:
            self.data = {}
        self.msg.data[key] = value

    def __getitem__(self, key):
        if self.msg.get(self.DATA) is None:
            raise MessageExp("data empty")
        value = self.msg.data.get(key)
        if value is None:
            raise KeyError(f"message no {key}")
        return value

    def value(self, key):
        return self.data.get(key)

    def _msg_checker(self):
        if self.msg.get(self.STATUS) is None:
            self.status = Status.SUCCESS
        if self.msg.get(self.REASON) is None:
            self.reason = ''

    @property
    def raw(self):
        return self.msg

    def __str__(self):
        self._msg_checker()
        return json_to_string(self.msg)

    __repr__ = __str__


class MessageExp(Exception):
    pass
