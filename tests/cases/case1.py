src = """
p = clf.predict([[100 * 1000, 10, 4]])

_arg0 = [[100 * 1000, 10, 4]]       # _arg0@4 <- {}
_attr_pred_0 = clf.predict          # _attr_pred_0@5 <- {clf@-1}
p = _attr_pred_0(_arg0)             # p@6 <- {_attr_pred_0@5, @_arg_0@4} (p depends just on the latest classifier)
del _arg0, _attr_pred_0

# stack machine in AST traversal order
push (store_in p)
push (getattr )
"""

s = 'p = clf.predict([[100 * 1000, 10, 4]])'

import dis
print(dis.dis(compile(s, '', mode='exec')))

"""
/Users/rogarcia/anaconda3/envs/gadget/bin/python /Users/rogarcia/git/inspectional-rara-parakeet/tests/cases/case1.py
  1           0 LOAD_NAME                0 (clf)
              2 LOAD_METHOD              1 (predict)
              4 BUILD_LIST               0
              6 LOAD_CONST               0 ((100000, 10, 4))
              8 LIST_EXTEND              1
             10 BUILD_LIST               1
             12 CALL_METHOD              1
             14 STORE_NAME               2 (p)
             16 LOAD_CONST               1 (None)
             18 RETURN_VALUE
None

Process finished with exit code 0
"""