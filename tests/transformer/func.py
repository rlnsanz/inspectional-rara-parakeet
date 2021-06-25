from gadget.transformer import transform_string

import unittest
import inspect
import ast
import astor


class TestFuncDefTransformer(unittest.TestCase):
    def test_simple_def(self):
        """
        original:
            def foo():
                return 42
        """
        # TODO: This test is driving bug fixes
        src = "\n".join(["def foo():", "\treturn 42", "forty = foo()"])

        sink = transform_string(
            src, self.__class__.__name__ + "." + inspect.currentframe().f_code.co_name
        )
        sink = astor.to_source(sink)

        print(sink)
        d = {}
        exec(sink, d, d)
        # print(d)
