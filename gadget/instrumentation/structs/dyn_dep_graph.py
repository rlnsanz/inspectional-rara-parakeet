from gadget.instrumentation.structs import state
from gadget.instrumentation.structs import ssa_table

import ast
import keyword
import builtins

tab = {}
lsn2s = {}
seq = []



class DataflowVisitor(ast.NodeVisitor):
    def __init__(self):
        self.edges = set([])

    def visit_Name(self, node):

        dlt = get_latest(node.id)
        if dlt is None:
            dlt = set([])
        else:
            lsn, s = dlt
            dlt = {lsn,}
        self.edges = self.edges.union(dlt)
        self.generic_visit(node)


def insert(name, text):
    # assert ssa_table.has_in(name) or keyword.iskeyword(name) or name in dir(builtins), name
    visitor = DataflowVisitor()
    visitor.visit(ast.parse(text))

    s = {state.lsn,}.union(visitor.edges)
    if name in tab:
        tab[name].append((state.lsn, s))
    else:
        tab[name] = [(state.lsn, s),]

    seq.append((name, state.lsn, s))
    lsn2s[state.lsn] = s


def get(name, lsn=None):
    pseq = tab.get(name, None)
    if lsn is None:
        return pseq
    fpseq = [s for _lsn, s in pseq if _lsn == lsn]
    if fpseq:
        assert len(fpseq) == 1
        return fpseq.pop()
    return None


def get_latest(name):
    pseq = get(name)
    if pseq:
        return pseq[-1]
    return None

def _helper_closure():
    ...

def trans_closure(name, sort=True):
    latest: set = get_latest(name)
    if latest is not None:
        # Fixpoint computation
        lsn, idb = latest
        accumulated = {lsn, }
        discovered = set(idb)
        while discovered:
            lsn = discovered.pop()
            if lsn not in accumulated:
                accumulated.add(lsn)
                discovered = discovered.union(lsn2s[lsn])
        if sort:
            return sorted(list(accumulated))
        return accumulated
    return None
