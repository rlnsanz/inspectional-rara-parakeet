from .utils import make_node

import ast
import astor


class RootCallTransformer(ast.NodeTransformer):
    def visit_Expr(self, node):
        """
        Expr(value)
        node.value is a Call
        """
        if not isinstance(node.value, ast.Call):
            return node
        src = astor.to_source(node.value)
        return make_node(
            f"ln.call({src}, text='''{src.strip()}''', line_no={node.lineno})"
        )
