from gadget.instrumentation.structs import state
from gadget.instrumentation.utils.stringify import print_ssa

import inspect


class tracking:
    """
    with ln.tracking('docs_training'):
        ...
    """
    def __init__(self, xp_name: str):
        self.xp_name = xp_name

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        self.main_filename = module.__file__

    def __enter__(self):
        print(f"STARTING experiment {self.xp_name} "
              f"by running script at {self.main_filename}")
        state.lsn += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'ENDING {self.xp_name}: last lsn {state.lsn}')
        print_ssa()
