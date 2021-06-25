from .utils import make_node

import ast
import astor


class AssignTransformer(ast.NodeTransformer):
    def visit_Assign(self, node):
        """
        Assign(targets, value, type_comment)
        """
        if len(node.targets) > 1:
            raise NotImplementedError("Assigning to multiple targets")
        src = astor.to_source(node.value)
        if isinstance(node.value, ast.Call):
            val = make_node(
                f"ln.call({src}, text='''{src.strip()}''', line_no={node.lineno})"
                f".assign(target='''{astor.to_source(node.targets[0]).strip()}''')"
            )
        else:
            val = make_node(
                f"ln.assign({src}, text='''{src.strip()}''', line_no={node.lineno}, "
                f"target='''{astor.to_source(node.targets[0]).strip()}''')"
            )
        node.value = val.value
        return node
