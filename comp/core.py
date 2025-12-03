from functools import reduce
from itertools import starmap as sm

def r(x):
   return next(sm(list, [sm(zip, [x])]))

def comp(f, g):
    return lambda x: f(g(x))
 
def comp_fun(*funcs):
    return reduce(comp, funcs, lambda x: x)
