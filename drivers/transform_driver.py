import ast
import astor

from gadget.transformer.utils import make_node, make_module_with
from gadget.transformer import RootCallTransformer, ImportingTransformer, AssignTransformer, FuncTransformer

# print(ast.dump(make_node("""
# def get_threshold(x, y):
#     with ln.func(name='get_threshold', args=None, ret_text='1970', line_no=12):
#         return 1970
# # ln.assign(get_threshold, 'get_threshold', 'get_threshold', line_no=21)
# """), indent=4))
# sys.exit(0)

callt = RootCallTransformer()
asgnt = AssignTransformer()
impt = ImportingTransformer()
funct = FuncTransformer()
with open('housing_prince_raw.py') as f:
    tree = ast.parse(f.read())
    stir_fry = ast.dump(tree, indent=4)
# transform calls
# transform assigns
# transform imports
# transform frames
# transform experiment
tree = callt.visit(tree)
tree = asgnt.visit(tree)
tree = impt.visit(tree)
tree = funct.visit(tree)
mod = make_module_with('housing_price', tree)
print(astor.to_source(mod))
print(stir_fry)
