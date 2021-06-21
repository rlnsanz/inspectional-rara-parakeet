from .utils import make_args, make_func_with, make_node

import ast
import astor


class FuncTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        name = node.name
        arguments = node.args
        if (arguments.posonlyargs or
            arguments.kwonlyargs or
            arguments.kw_defaults or
            arguments.defaults):
            raise NotImplementedError(arguments)
        args = make_args([a.arg for a in arguments.args])
        ret_text = None
        for stmt in reversed(node.body):
            if isinstance(stmt, ast.Return):
                ret_text = astor.to_source(stmt.value)
                break
        weeth = make_func_with(name, args, node.lineno, ret_text.strip())
        weeth.body = node.body
        node.body = [weeth, ]
        return node

        # next_node = make_node(f"ln.assign({name}, text='''{name}''', line_no={node.lineno}, "
        #                      f"target='''{name}''')")
        # assert isinstance(next_node, ast.Expr), type(next_node)
        #
        # return [node, next_node]
