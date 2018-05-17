from shiny.html5 import Element
import random


_ALAPHA = "abcdefghijklmnopqrstuvwxyz"
_DIGIT = "0123456789"
_STR = _ALAPHA + _DIGIT


def ran_str(k=5, safe=False):
    return random.choice(_ALAPHA) if safe else "" + \
           "".join(random.choices(_STR, k=k))


def test_element():
    h1 = Element("h1")
    text = ran_str(5)
    id = ran_str(10)

    h1.id = id
    assert h1.get("id") == id
    assert h1.id == id

    h1.text = text

    key = ran_str(safe=True)
    value = ran_str()
    h1.set(key, value)

    assert h1.get(key) == value
