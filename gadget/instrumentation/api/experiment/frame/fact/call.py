from gadget.instrumentation.structs import state
from gadget.instrumentation.structs import dyn_dep_graph
from gadget.instrumentation.utils import stringify
from . import assign

import re
import ast


class Call:
    # TODO: method chaining design
    # TODO: you can call a call. Modify class Call
    def __init__(self, pe, text, line_no):
        """
        pe: parenthetical expression. e.g. `foo()`
        """
        self.pe = pe
        self.text = text
        self.line_no = line_no

    def assign(self, target):
        assign(self.pe, target, self.text, line_no=self.line_no)
        return self.pe

    def __lt__(self, other):
        return other > self.pe

    def __gt__(self, other):
        return self.pe > other

    def __le__(self, other):
        return other >= self.pe

    def __ge__(self, other):
        return self.pe >= other


class ReturnError(RuntimeError):
    pass


class CallGetter(ast.NodeVisitor):
    def visit_Call(self, node):
        foo = node.func
        if isinstance(foo, str):
            raise ReturnError(foo)
        else:
            assert type(foo).__name__ in dir(ast)
            raise ReturnError(ast.unparse(foo))


def get_caller(full_text):
    g = CallGetter()
    try:
        g.visit(ast.parse(full_text))
    except ReturnError as e:
        return e.args[0]

def get_name(full_text):
    # TODO: make field sensitive
    caller = get_caller(full_text)
    return caller.split('.')[0]

def call(pe, text, line_no):
    #TODO: make field sensitives
    t = text.replace('\n', '')
    t = re.sub(r"""\s(\s)+""", "", t)
    name = get_name(t)
    dyn_dep_graph.insert(name, t)
    c = Call(pe, text, line_no)
    print(f"{stringify.vertical_prefix_string()}CALL {t}: "
          f"evaluated\t\t{line_no}:{state.lsn}")
    state.lsn2line_no[state.lsn] = line_no
    state.lsn += 1
    return c