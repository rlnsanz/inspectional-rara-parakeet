import json


class SSA:
    _tab = {}
    _seq = []


class SerializationCapsule:
    """
    Serialization Capsule
    """
    def __init__(self, v):
        self.v = v
        self.out = None
        self.mode = None

    def dump(self):
        if self.out is not None:
            return self.out
        try:
            self.out = json.dumps(self.v)
            self.mode = 'json'
        except TypeError as e:
            self.out = str(type(self.v))
            self.mode = None
        finally:
            del self.v  # garbage collect
            return self.out

    def load(self):
        if self.mode is None:
            assert self.out is not None
            return self.out
        elif self.mode == 'json':
            return json.loads(self.out)
        raise NotImplementedError()

    def __str__(self):
        return self.out

    def __repr__(self):
        return self.out


def insert(name, idx, v):
    assert isinstance(name, str)
    _id = id(v)
    if 'numpy' in str(type(v)):
        v = v.tolist()
    capsule = SerializationCapsule(v)
    capsule.dump()
    group = (idx, capsule)
    if name in SSA._tab:
        SSA._tab[name].append(group)
    else:
        SSA._tab[name] = [group, ]
    SSA._seq.append((name, idx, capsule))


def get(name, force_value=True):
    if name in SSA._tab:
        idx, v = SSA._tab[name][-1]
        if force_value:
            assert v.mode is not None  # it's possible to deserialize v with a load
        return idx, v.load()
    return None


def as_seq():
    for (name, idx, capsule) in SSA._seq:
        yield (name, idx, capsule.load())


def has_in(name):
    return name in SSA._tab