from gadget.transformer.call import RootCallTransformer
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

        """
        # TODO: This test is driving bug fixes
        src = 'np.random.seed(randint(0,100))'
        tree = RootCallTransformer().visit(ast.parse(src))
        node = tree.body[-1]

        template = '\n'.join([
            "from random import randint",
            "import numpy as np",
            "import gadget as ln",
            f"with ln.tracking('{self.__class__.__name__ + '.' + inspect.currentframe().f_code.co_name}'):",
            f"\t{astor.to_source(tree)}"
        ])

        self.assertIsInstance(node.value, ast.Expr)

        print(template)
        exec(template, {}, {})


