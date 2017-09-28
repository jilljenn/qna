import sympy as sp

X1 = sp.Symbol('X1')
Y = sp.Symbol('Y')
Th = sp.Symbol('Th')
th_bias = sp.Symbol('th_bias')

N = 5
n = 6
p = 2

# X1 = sp.MatrixSymbol('X1', N, p)
# Y = sp.MatrixSymbol('Y', N, n)
# Th = sp.MatrixSymbol('Th', n, p)

# One = sp.ones(N, n)

def proba1(Th, X1):
    return 1 / (1 + sp.exp(-X1 * Th - th_bias))

def loglikelihood(Th, X1):
    return (1 - Y) * sp.log(1 - proba1(Th, X1)) + Y * sp.log(proba1(Th, X1))

def score(Th, X1):
    return loglikelihood(Th, X1).diff(Th)

def hessian(Th, X1):
    return loglikelihood(Th, X1).diff(Th).diff(Th)    

def display(expr):
    # sp.pprint(expr)
    sp.pprint(sp.simplify(expr))

# display(sp.log(proba1(Th, X1)))
# display(sp.log(proba1(Th, X1)).diff(Th))
# display(sp.log(1 - proba1(Th, X1)))
# print('wow')
# display(sp.log(1 - proba1(Th, X1)).diff(Th))

print('Loglikelihood')
display(loglikelihood(Th, X1))
print('Score')
display(score(Th, X1))
print('by bias')
display(loglikelihood(Th, X1).diff(th_bias))
print('Hessian')
display(hessian(Th, X1))
print('by bias')
display(loglikelihood(Th, X1).diff(th_bias).diff(th_bias))
