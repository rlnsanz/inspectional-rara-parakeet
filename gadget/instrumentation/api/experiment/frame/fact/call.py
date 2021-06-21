from gadget.instrumentation.structs import state
from gadget.instrumentation.structs import dyn_dep_graph
from gadget.instrumentation.utils import stringify

import re
import ast


# class CallGetter(ast.NodeVisitor):
#
#     def __init__(self):
#         self.active = False
#         self.names = set([])
#
#     def visit_Name(self, node):
#         """
#         x() -> x
#         assets['foo']() -> assets
#         assets.attr['foo']() -> assets
#         assets[wot['m8']]() -> assets, wot
#         """
#         if self.active:
#             self.names.add(node.id)
#         self.generic_visit(node)
#
#     def visit_Call(self, node):
#         active = self.active
#         self.active = True
#         self.generic_visit(node)
#         self.active = active
#
#
# def get_caller(full_text):
#     g = CallGetter()
#     try:
#         g.visit(ast.parse(full_text))
#     except ReturnError as e:
#         return e.args[0]
#
# def get_name(full_text):
#     # TODO: make field sensitive
#     caller = get_caller(full_text)
#     return caller.split('.')[0]

def call(pe, text, line_no):
    #TODO: make field sensitives
    t = text.replace('\n', '')
    t = re.sub(r"""\s(\s)+""", "", t)
    dyn_dep_graph.insert(t)
    print(f"{stringify.vertical_prefix_string()}CALL {t}: "
          f"evaluated\t\t{line_no}:{state.lsn}")
    state.lsn2line_no[state.lsn] = line_no
    state.lsn += 1
    return pe