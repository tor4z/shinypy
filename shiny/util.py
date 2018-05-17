import random


_DIGIT = '0123456789'
_ALAPHA = 'abcdefghijklmnopqrstuvwxyz'
_PRINTABLE = _DIGIT + _ALAPHA


def randstr(k=5):
    k = k-1
    return '_' + ''.join(random.choices(_PRINTABLE, k=k)) if k > 0 else ''
