import json
import random
from shiny.message import Message, Status, Method
from shiny.util import randstr


def test_str_msg_parser():
    msg = {}
    data = {}

    for _ in range(10):
        data[randstr(5)] = randstr(5)

    reason = randstr(10)
    msg['status'] = Status.SUCCESS
    msg['reason'] = reason
    msg['data'] = data
    m = Message(msg)

    assert m.data == data
    assert m.status == Status.SUCCESS
    assert m.reason == reason
    assert m.keys == data.keys()

    for key in data.keys():
        assert m.value(key) == data.get(key)

    str_msg = json.dumps(msg)
    m = Message(str_msg)

    assert m.data == data
    assert m.status == Status.SUCCESS
    assert m.reason == reason
    assert m.keys == data.keys()

    for key in data.keys():
        assert m.value(key) == data.get(key)


def test_msg_get():
    key = randstr(5)
    msg = Message()
    msg.query(key)
    target = {'method': Method.GET,
              'data': {'keys': [key]}}

    assert msg.raw == target


def test_msg_get_multi_keys():
    keys = []
    for _ in range(random.randint(10, 20)):
        keys.append(randstr(5))

    msg = Message()
    msg.query(keys)
    target = {'method': 'GET',
              'data': {'keys': keys}}

    assert msg.raw == target
