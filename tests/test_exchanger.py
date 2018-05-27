import random
from shiny.exchanger import Mapping
from shiny.util import randstr


def test_mapping():
    ins = []
    outs = []

    cnt = 5 * 8

    for _ in range(cnt):
        ins.append(randstr(5))
        outs.append(randstr(5))

    mapping = Mapping()

    out_ports = random.sample(outs, k=int(cnt/4))
    for out_port in out_ports:
        in_ports = random.sample(ins, k=int(cnt/8))
        for in_port in in_ports:
            mapping.bind(in_port, out_port)

    for out_port in outs:
        in_ports = mapping.get_ins(out_port)
        for in_port in in_ports:
            assert out_port in mapping.get_outs(in_port)
