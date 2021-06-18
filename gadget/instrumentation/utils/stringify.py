from gadget.instrumentation.structs import state, ssa_table, dyn_dep_graph


def vertical_prefix_string():
    msg = ''
    for each in range(state.depth):
        msg += "|    "
    return msg


def print_ssa():
    print('\nSSA')
    for name, lsn, v in ssa_table.as_seq():
        # print(f"{(name, idx, v)}\n{f'# {dyn_dep_graph.get(name, idx)}' if dyn_dep_graph.get(name, idx) else ''}")
        print(f"{(name, lsn, v)}")
    print('\nDDG:')
    for name, lsn, deps in dyn_dep_graph.seq:
        print((name, lsn, deps))

    debug = {
        'name': 'p'
    }
    print(f"\ntransitive closure {debug['name']}:")
    tclosure = dyn_dep_graph.trans_closure(debug['name'])
    print("Sequence of LSNs: ", tclosure)
    print("Sequence of LINE_NOs: ", sorted(list(set([state.lsn2line_no[each] for each in tclosure]))))
