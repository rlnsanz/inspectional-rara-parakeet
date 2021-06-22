from gadget.transformer import transform

import astor
import unittest


tree_transformed = transform('embeddingsA2.py', 'embeddiangsA2', exept=None)

class ShoppeeTester(unittest.TestCase):

    def test_transform(self):
        print(astor.to_source(tree_transformed))

    def test_ast_tree(self):
        print(astor.dump_tree(tree_transformed))

    def test_exec(self):
        d = {}
        exec(astor.to_source(tree_transformed), d, d)