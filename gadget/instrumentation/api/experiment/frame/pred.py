from gadget.instrumentation.structs import state
from gadget.instrumentation.utils import stringify


class pred:
    _stack = []

    @staticmethod
    def new(predicate, text, name, line_no):
        pred._stack.append({'predicate': predicate, 'text': text, 'name': name, 'line_no': line_no})
        print(f"{stringify.vertical_prefix_string()}COND_IN {name}: {text} evaluates to {predicate}\t\t{line_no}:{state.lsn}")
        state.lsn2line_no[state.lsn] = line_no
        state.lsn += 1
        state.depth += 1
        return predicate

    @staticmethod
    def pop():
        d = pred._stack.pop()
        state.depth -= 1
        print(f"{stringify.vertical_prefix_string()}COND_OUT {d['name']}: exiting condition {d['name']}")
        state.lsn += 1
