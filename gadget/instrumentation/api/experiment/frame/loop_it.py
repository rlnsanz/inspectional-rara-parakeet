from gadget.instrumentation.structs import state
from gadget.instrumentation.utils import stringify
from gadget.instrumentation.api.experiment.frame.fact import assign


class loop_it:
    _stack = []

    @staticmethod
    def new(iter8r, text, name, line_no):
        loop_it._stack.append({"iter8r": iter8r, "text": text, "name": name})
        assign_target, assign_text = text.split(" in ")
        print(
            f"{stringify.vertical_prefix_string()}LOOP_IN {name}: "
            f"iterating for each {assign_target} in {iter8r}\t\t{line_no}:{state.lsn}"
        )
        state.lsn2line_no[state.lsn] = line_no
        state.lsn += 1
        state.depth += 1
        i = 0
        for each in iter8r:
            print(
                f"{stringify.vertical_prefix_string()}****LOOP_ITERATION {name}@{i}: "
                f"iterator element {assign_text}[{i}] "
                f"in loop {name}\t\t{line_no}:{state.lsn}"
            )
            state.lsn2line_no[state.lsn] = line_no
            state.lsn += 1
            assign(each, assign_target, f"{assign_text}[{i}]", line_no)
            yield each
            i += 1

    @staticmethod
    def pop():
        d = loop_it._stack.pop()
        state.depth -= 1
        print(
            f"{stringify.vertical_prefix_string()}LOOP_OUT {d['name']}: loop {d['name']} ended"
        )
        state.lsn += 1
