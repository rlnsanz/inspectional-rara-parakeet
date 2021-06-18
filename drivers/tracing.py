"""
import numpy as np      # line_no: 1
import gadget

gadget.record('docs_training_py')

x = np.arange(5)        # line_no: 2

s = x[0]                # line_no: 3
for i in x:             # line_no: 4
    if i % 2 == 0:      # line_no: 5
        s += i          # line_no: 6

print('done')
"""
import gadget as ln

with ln.tracking('docs_training_py3'):
    import numpy as np
    ln.importing(np, module='numpy', name='np', line_no=1)

    x = ln.call(np.arange(5), args=(5, '5'), text='np.arange(5)', line_no=2).assign(target='x')

    s = ln.assign(x[0], text='x[0]', target='s', line_no=3)
    for i in ln.loop_it.new(x, text='i in x', name='main_loop', line_no=4):
        if ln.pred.new(i % 2 == 0, text='i % 2 == 0', name='main_cond', line_no=5):
            s += ln.assign(i, target='s', text='i', mod='+=', line_no=6)
        ln.pred.pop()
    ln.loop_it.pop()

    # ln.call(eval(f'done'), args=('done', "'done'"), text="eval('done')")