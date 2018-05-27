import random
import json


_DIGIT = '0123456789'
_ALAPHA = 'abcdefghijklmnopqrstuvwxyz'
_PRINTABLE = _DIGIT + _ALAPHA


def randstr(k=5):
    k = k-1
    return '_' + ''.join(random.choices(_PRINTABLE, k=k)) if k > 0 else ''


def json_to_string(data):
    return json.dumps(data)


def string_to_json(string):
    return json.loads(string)
