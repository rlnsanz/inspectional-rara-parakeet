from gadget.instrumentation.structs import state
from gadget.instrumentation.utils import stringify
from gadget.instrumentation.structs import dyn_dep_graph
from gadget.instrumentation.structs import ssa_table


def assign(e, target, text, line_no, mod=None):
    if mod is None:
        print(f"{stringify.vertical_prefix_string()}ASSIGN {target}: "
              f"assigning {text}, into {target}\t\t{line_no}:{state.lsn}")
        ssa_table.insert(target, state.lsn, e)
        dyn_dep_graph.insert(target, text)
    elif mod == '+=':
        print(f"{stringify.vertical_prefix_string()}ASSIGN {target}: "
              f"incrementing {target} by {text}\t\t{line_no}:{state.lsn}")
        ssa_table.insert(target, state.lsn, e + ssa_table.get(target)[1])
        dyn_dep_graph.insert(target, f"{target} + {text}")
    else:
        raise NotImplementedError()
    state.lsn2line_no[state.lsn] = line_no
    state.lsn += 1
    return e
