from .assign import AssignTransformer
from .call import RootCallTransformer
from .func import FuncTransformer
from .importing import ImportingTransformer

# TODO: Add support for Tuples
import ast
from .utils import make_module_with

import astor


def transform_string(s: str, experiment_name: str):
    tree = ast.parse(s)
    for transformer in [RootCallTransformer(), AssignTransformer(), ImportingTransformer(), FuncTransformer()]:
        tree = transformer.visit(tree)
        print(astor.to_source(tree))

    return make_module_with(experiment_name, tree)


__all__ = [
    'AssignTransformer',
    'RootCallTransformer',
    'FuncTransformer',
    'ImportingTransformer',
    'transform_string'
]








