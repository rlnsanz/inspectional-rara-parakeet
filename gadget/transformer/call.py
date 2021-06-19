from .utils import make_node

import ast
import astor


class RootCallTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        new_node = self.generic_visit(node)
        src = astor.to_source(new_node)
        return make_node(f"ln.call({src}, text='''{src.strip()}''', line_no={node.lineno}).pe")

    def visit_Expr(self, node):
        """
        Expr(value)
        node.value is a Call
        """
        if isinstance(node.value, ast.Call):
            node.value = self.visit(node.value)
        return node
