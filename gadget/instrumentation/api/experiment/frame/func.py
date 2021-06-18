from gadget.instrumentation.structs import state
from gadget.instrumentation.utils import stringify


class func:
    def __init__(self, name, line_no, args=None, ret_text=None):
        self.name = name
        if args is None:
            args = []
        self.args = args
        self.ret_text = ret_text
        self.line_no = line_no

    def __enter__(self):
        print(f"{stringify.vertical_prefix_string()}FUNC_IN: "
              f"stepping into function {self.name} "
              f"with {len(self.args)} arguments.\t\t{self.line_no}:{state.lsn}")
        state.lsn2line_no[state.lsn] = self.line_no
        state.depth += 1
        state.lsn += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        state.depth -= 1
        print(f"{stringify.vertical_prefix_string()}FUNC_OUT: "
              f"function {self.name} "
              f"returning {'nothing' if self.ret_text is None else self.ret_text}")
        state.lsn += 1
