from .assign import AssignTransformer
from .call import RootCallTransformer
from .func import FuncTransformer
from .importing import ImportingTransformer

# TODO: Add support for Tuples
import ast
from .utils import make_module_with

import astor


def transform_string(s: str, experiment_name: str, exept=None):
    tree = ast.parse(s)
    transformers = ['Assign', 'RootCall', 'Func', 'Importing']
    if exept is not None:
        assert isinstance(exept, list)
        transformers = [each for each in transformers if each not in exept]
    for transformer in [eval(f'{each}Transformer()') for each in transformers]:
        tree = transformer.visit(tree)
    return make_module_with(experiment_name, tree)


def transform(path: str, experiment_name, exept=None):
    with open(path, 'r') as f:
        return transform_string(f.read(), experiment_name, exept)

__all__ = [
    'AssignTransformer',
    'RootCallTransformer',
    'FuncTransformer',
    'ImportingTransformer',
    'transform_string'
]








