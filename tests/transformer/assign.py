from gadget.transformer.assign import AssignTransformer

import unittest
import inspect
import ast
import astor

prefix = """
import gadget as ln
with ln.tracking('{xp_name}'):
    {assign_string}
    {instrumented_string}
"""


class TestAssignTransformer(unittest.TestCase):
    def test_value(self):
        src = "x = 42"

        tformer = AssignTransformer()
        tree = tformer.visit(ast.parse(src))
        node = tree.body[-1]

        self.assertIsInstance(node, ast.Assign)

        filled_py = prefix.format(
            xp_name=self.__class__.__name__
            + "."
            + inspect.currentframe().f_code.co_name,
            assign_string=src,
            instrumented_string=astor.to_source(node),
        )

        print(filled_py)
        exec(filled_py, {}, {})

    def test_loc(self):
        src = "x = y"

        tformer = AssignTransformer()
        tree = tformer.visit(ast.parse(src))
        node = tree.body[-1]

        self.assertIsInstance(node, ast.Assign)

        filled_py = prefix.format(
            xp_name=self.__class__.__name__
            + "."
            + inspect.currentframe().f_code.co_name,
            assign_string=src,
            instrumented_string=astor.to_source(node),
        )

        print(filled_py)
        # NameError: name 'y' is not defined
        self.assertRaises(NameError, exec, filled_py, {}, {})

        exec(filled_py, {"y": 42}, {"y": 42})
