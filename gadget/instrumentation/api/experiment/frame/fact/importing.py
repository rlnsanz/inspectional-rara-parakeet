from gadget.instrumentation.structs import state
from . import assign

import inspect


def importing(o, module, name, line_no):
    #TODO: add to dataflow
    # ssa_table.insert(name, state.lsn, o)
    """
    o: the object corresponding to the imported module
    """
    print(f"IMPORT {module}: "
          f"successfully imported {module} "
          f"from {inspect.getfile(o)}\t\t{line_no}:{state.lsn}")
    state.lsn2line_no[state.lsn] = line_no
    state.lsn += 1
    assign(o, name, name, line_no)



