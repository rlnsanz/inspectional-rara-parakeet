from gadget.instrumentation.structs import state

import ast

tab = {}
lsn2s = {}
seq = []

"""
TODO: Will have to work with AST store and Load

"""


class DataflowVisitor(ast.NodeVisitor):
    def __init__(self, carry=None):
        if carry is None:
            self.reads = set([])
        else:
            self.reads = carry
        self.writes = set([])

    def visit_Name(self, node):
        self.generic_visit(node)

        dlt = get_latest(node.id)
        if dlt is None:
            dlt = set([])
        else:
            lsn, s = dlt
            dlt = {lsn,}
        self.reads = self.reads.union(dlt)

        if isinstance(node.ctx, ast.Store):
            print('********************************************************************')
            s = {state.lsn, }.union(self.reads)
            if node.id in tab:
                tab[node.id].append((state.lsn, s))
            else:
                tab[node.id] = [(state.lsn, s), ]
            seq.append((node.id, state.lsn, s))
            lsn2s[state.lsn] = s
            state.lsn += 1
            self.writes.add(node.id)


def insert(text):
    # assert ssa_table.has_in(name) or keyword.iskeyword(name) or name in dir(builtins), name
    visitor = DataflowVisitor()
    visitor.visit(ast.parse(text))


def get(name=None, lsn=None):
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
