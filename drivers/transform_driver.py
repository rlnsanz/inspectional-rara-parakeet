import gadget as ln
with ln.tracking('TestFuncDefTransformer.test_simple_def'):

    def foo():
        with ln.func(name='foo', args=[], ret_text='42', line_no=1):
            return 42
    # ln.assign(foo, text='foo', line_no=1, target='foo')
    forty = ln.call(foo(), text='foo()', line_no=3).assign(target='forty')