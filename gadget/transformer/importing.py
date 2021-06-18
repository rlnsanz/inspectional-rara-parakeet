from .utils import make_node

import ast


class ImportingTransformer(ast.NodeTransformer):
    def visit_Import(self, node):
        """
        Import(names)
        """
        stmts = [node,]
        for alias in node.names:
            inst_node = make_node(f"ln.importing({alias.asname if alias.asname else alias.name}, "
                                  f"module='{alias.name}', name='{alias.asname if alias.asname else alias.name}', "
                                  f"line_no={node.lineno})")
            stmts.append(inst_node)
        return stmts

    def visit_ImportFrom(self, node):
        """
        ImportFrom(module, names, level)
        """
        stmts = [node, ]
        for alias in node.names:
            inst_node = make_node(f"ln.importing({alias.asname if alias.asname else alias.name}, "
                                  f"module='{node.module}', name='{alias.asname if alias.asname else alias.name}', "
                                  f"line_no={node.lineno})")
            stmts.append(inst_node)
        return stmts
