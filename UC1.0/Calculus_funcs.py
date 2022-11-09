import sympy as sp

def differentation(f, order = 1):
    try:
        order = int(order)
        while order > 0:
            x = sp.Symbol("x")
            f = sp.diff(f, x)
            order = order - 1
        while ("**" in str(f)):
            f = str(f).replace("**", "^")
        return f
    except:
        return "MATH ERROR"

def integration(f, order = 1):
    try:
        order = int(order)
        while order > 0:
            x = sp.Symbol("x")
            f = sp.integrate(f, x)
            order = order - 1
        while ("**" in str(f)):
            f = str(f).replace("**", "^")
        return f
    except:
        return "MATH ERROR"


def integration_limits(f, a, b, order = 1):
    try:
        order, a, b = int(order), float(a), float(b)
        while order > 0:
            x = sp.Symbol("x")
            f = sp.integrate(f, (x, a, b))
            order = order - 1
        while ("**" in str(f)):
            f = str(f).replace("**", "^")
        return f
    except:
        return "MATH ERROR"
    