from gadget.transformer import transform_string
from gadget.transformer.assign import AssignTransformer

import unittest
import inspect
import ast
import astor


class TestCallTransformer(unittest.TestCase):

    def test_assign_call(self):
        src = 'x = np.arange(5)'
        tree = AssignTransformer().visit(ast.parse(src))
        node = tree.body[-1]

        template = '\n'.join([
            "import numpy as np",
            "import gadget as ln",
            f"with ln.tracking('{self.__class__.__name__ + '.' + inspect.currentframe().f_code.co_name}'):",
            f"\t{astor.to_source(node)}"
        ])

        self.assertIsInstance(node, ast.Assign)
        self.assertIsInstance(node.value, ast.Call)

        print(template)
        exec(template, {}, {})

    def test_root_call(self):
        """
        original:
            np.random.seed(randint(0,100))
        bytecode:
            _arg0 = randint(0, 100)
            np.random.seed(_arg0)
        """
        # TODO: This test is driving bug fixes
        src = '\n'.join([
            "from random import randint",
            "import numpy as np",
            '_arg0 = randint(0,100)',
            'np.random.seed(_arg0)'
        ])

        sink = transform_string(src, self.__class__.__name__ + '.' + inspect.currentframe().f_code.co_name)
        sink = astor.to_source(sink)

        print(sink)
        exec(sink, {}, {})




