import ast

from gadget.transformer.visitors import get_change_and_read_set, LoadStoreDetector, StatementCounter
from gadget.transformer.code_gen import *
from gadget.transformer.utils import set_intersection, set_union, node_in_nodes
import copy
import astor
import os

# line_no = 0
#
#
# def get_line_no():
#     global line_no
#     old = line_no
#     line_no += 1
#     return old

# TODO: Add support for Tuples


def make_node(text):
    mod = ast.parse(text)
    assert len(mod.body) == 1
    return mod.body.pop()

def make_args(args):
    """
    ['col'] -> [(col, 'col')]
    """
    s = '['
    for arg in args:
        s += f'''({arg}, "{arg}"),'''
    s += ']'
    return s


def make_func_with(name, args, line_no, ret_text=None):
    if ret_text is not None:
        s = f"""with ln.func(name='{name}', args={args}, ret_text='''{ret_text}''', line_no={line_no}):\n\tpass"""
    else:
        s = f"""with ln.func(name='{name}', args={args}, line_no={line_no}):\n\tpass"""
    mod = ast.parse(s)
    return mod.body.pop()


def make_module_with(text):
    s = f"""import gadget as ln\nwith ln.tracking('{text}'):\n\tpass"""
    mod = ast.parse(s)
    return mod


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

        next_node = make_node(f"ln.assign({name}, text='''{name}''', line_no={node.lineno}, "
                             f"target='''{name}''')")
        assert isinstance(next_node, ast.Expr), type(next_node)

        return [node, next_node]


class AssignTransformer(ast.NodeTransformer):
    def visit_Assign(self, node):
        """
        Assign(targets, value, type_comment)
        """
        if len(node.targets) > 1:
            raise NotImplementedError("Assigning to multiple targets")
        src = astor.to_source(node.value)
        if isinstance(node.value, ast.Call):
            val = make_node(f"ln.call({src}, text='''{src.strip()}''', line_no={node.lineno})"
                             f".assign(target='''{astor.to_source(node.targets[0]).strip()}''')")
        else:
            val = make_node(f"ln.assign({src}, text='''{src.strip()}''', line_no={node.lineno}, "
                             f"target='''{astor.to_source(node.targets[0]).strip()}''')")
        node.value = val.value
        return node


class RootCallTransformer(ast.NodeTransformer):
    def visit_Expr(self, node):
        """
        Expr(value)
        node.value is a Call
        """
        if not isinstance(node.value, ast.Call):
            return node
        src = astor.to_source(node.value)
        return make_node(f"ln.call({src}, text='''{src.strip()}''', line_no={node.lineno})")


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


class Transformer(ast.NodeTransformer):
    static_key = 0

    class RefuseTransformError(RuntimeError):
        pass

    @staticmethod
    def transform(filepaths, inplace=False, root_script=None):

        if not isinstance(filepaths, list):
            root_script = filepaths
            filepaths = [filepaths,]
        elif len(filepaths) == 1:
            root_script = filepaths[0]

        for filepath in filepaths:
            with open(filepath, 'r') as f:
                contents = f.read()
            transformer = Transformer()
            new_contents = transformer.visit(ast.parse(contents))
            new_contents.body.insert(0, ast.Import(names=[ast.alias('flor', asname=None)]))
            if root_script and os.path.samefile(filepath, root_script):
                new_contents.body.append(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=ast.Attribute(value=ast.Name('flor'), attr='SKIP')),
                                                body=[ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name('flor'), attr='flush'),
                                                                              args=[], keywords=[]))], orelse=[]))
            new_contents = astor.to_source(new_contents)
            new_filepath, ext = os.path.splitext(filepath)
            new_filepath += ('_transformed' if not inplace else '') + ext
            with open(new_filepath, 'w') as f:
                f.write(new_contents)
            print(f"wrote {new_filepath}")

    def __init__(self):
        # These are names defined before the loop
        # If these values are updated in the loop body, we want to save them
        #       Even if they look like "blind writes"
        self.assign_updates = []

        # Loop_Context
        #   Are we in a loop context?
        self.loop_context = False

    def get_incr_static_key(self):
        sk = Transformer.static_key
        Transformer.static_key += 1
        return sk

    def visit_Assign(self, node):
        lsd = LoadStoreDetector(writes=self.assign_updates)
        lsd.visit(node)
        lsd = LoadStoreDetector()
        [lsd.visit(n) for n in node.targets]
        output = [self.generic_visit(node), ]
        for name in lsd.writes:
            output.append(make_test_force(name))
        return output

    def visit_FunctionDef(self, node):
        temp = self.assign_updates
        self.assign_updates = []
        lsd = LoadStoreDetector(writes=self.assign_updates)
        lsd.visit(node.args)                                # This is possibly redundant but harmless because of set semantics of lsd
        output = self.generic_visit(node)
        self.assign_updates = temp

        output.body = [make_block_initialize('namespace_stack'), ] + output.body

        output.body = [ast.Try(body=output.body,
                              handlers=[],
                              orelse=[],
                              finalbody=[make_block_destroy('namespace_stack')]), ]

        return output

    def visit_Expr(self, node):
        if self.loop_context and is_side_effecting(node) and not is_expr_excepted(node):
            # In the context of a MAY-MEMOIZE loop
            raise self.RefuseTransformError()
        return self.generic_visit(node)

    def _vistit_loop(self, node):
        lsd_change_set, mcd_change_set, read_set = get_change_and_read_set(node)
        change_set = set_union(lsd_change_set, mcd_change_set)
        memoization_set = set_intersection(set_union(self.assign_updates, read_set), change_set)    # read_set: unmatched_reads

        new_node = self.generic_visit(node)

        if not memoization_set:
            #TODO: should probably raise a RefuseTransformError
            return new_node

        underscored_memoization_set = []
        for element in memoization_set:
            if not node_in_nodes(element, mcd_change_set):
                underscored_memoization_set.append(element)
            else:
                underscored_memoization_set.append(ast.Name('_', ast.Store()))

        # Outer Block
        block_initialize = make_block_initialize('skip_stack', [make_arg(self.get_incr_static_key()),])
        cond_block = make_cond_block()
        proc_side_effects = make_proc_side_effects(underscored_memoization_set,
                                                   memoization_set)

        cond_block.body = [new_node, ]

        return [block_initialize, cond_block, proc_side_effects]

    def proc_loop(self, node):
        temp = self.loop_context

        sc = StatementCounter()
        sc.visit(node)
        if sc.count <= 3:
            # import astor
            # print(astor.to_source(node))
            self.loop_context = False
            noud = self.generic_visit(node)
            self.loop_context = temp

            blinit = make_block_initialize('skip_stack', [make_arg(self.get_incr_static_key()), make_arg(0)])
            blestroy = make_block_destroy('skip_stack')

            return [blinit, noud, blestroy]


        self.loop_context = True

        temp_assign_updates = list(self.assign_updates)
        node_clone = copy.deepcopy(node)

        try:
            new_node = self._vistit_loop(node)
            return new_node
        except self.RefuseTransformError:
            if temp:
                raise
            self.loop_context = False
            self.assign_updates = temp_assign_updates
            new_node = self.generic_visit(node_clone)

            blinit = make_block_initialize('skip_stack', [make_arg(self.get_incr_static_key()), make_arg(0)])
            blestroy = make_block_destroy('skip_stack')

            return [blinit, new_node, blestroy]
        except AssertionError as e:
            print(f"Assertion Error: {e}")
            return ast.NodeTransformer().generic_visit(node)
        finally:
            self.loop_context = temp



    def visit_For(self, node):
        return self.proc_loop(node)

    def visit_While(self, node):
        return self.proc_loop(node)

