from gadget.instrumentation.structs import state
from gadget.instrumentation.structs.ssa_table import SSA
from gadget.instrumentation.utils.stringify import print_ssa
from gadget.shelf import mk_job

import inspect


class tracking:
    """
    with ln.tracking('docs_training'):
        ...
    """

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        mk_job(experiment_name)

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        self.main_filename = module.__file__ if hasattr(module, "__file__") else "..."

    def __enter__(self):
        print(
            f"STARTING experiment {self.experiment_name} "
            f"by running script at {self.main_filename}"
        )
        state.lsn += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"ENDING {self.experiment_name}: last lsn {state.lsn}")

        SSA.logger.close()
        # TODO: Serialize the SSA and DDG for debugging.

        print_ssa()
