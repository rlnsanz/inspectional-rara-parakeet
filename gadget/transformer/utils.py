import ast


def make_node(text):
    mod = ast.parse(text)
    assert len(mod.body) == 1
    return mod.body.pop()


def make_args(args):
    """
    ['col'] -> [(col, 'col')]
    """
    s = "["
    for arg in args:
        s += f"""({arg}, "{arg}"),"""
    s += "]"
    return s


def make_func_with(name, args, line_no, ret_text=None):
    if ret_text is not None:
        s = f"""with ln.func(name='{name}', args={args}, ret_text='''{ret_text}''', line_no={line_no}):\n\tpass"""
    else:
        s = f"""with ln.func(name='{name}', args={args}, line_no={line_no}):\n\tpass"""
    mod = ast.parse(s)
    return mod.body.pop()


def make_module_with(experiment_name, tree):
    s = f"""import gadget as ln\nwith ln.tracking('{experiment_name}'):\n\tpass"""
    mod = ast.parse(s)
    mod.body[-1].body = [
        tree,
    ]
    return mod
