from gadget.logger import Logger
from gadget.journal.entry import DataRef, DataVal
# import json


class SSA:
    _tab = {}
    _seq = []
    logger = None


def insert(name, idx, v):
    assert isinstance(name, str)
    if SSA.logger is None:
        SSA.logger = Logger()
    _id = id(v)

    capsule = DataVal(name, idx, v) if type(v) in [type(None), int, float, bool, str] else DataRef(name, idx, v)

    group = (idx, capsule)
    if name in SSA._tab:
        SSA._tab[name].append(group)
    else:
        SSA._tab[name] = [group, ]
    SSA._seq.append((name, idx, capsule))
    SSA.logger.append(capsule)


def get(name, force_value=True):
    if name in SSA._tab:
        idx, v = SSA._tab[name][-1]
        if force_value:
            assert v.mode is not None  # it's possible to deserialize v with a load
        return idx, v.make_val()
    return None


def as_seq():
    for (name, idx, capsule) in SSA._seq:
        yield (name, idx, capsule.make_val())


def has_in(name):
    return name in SSA._tab