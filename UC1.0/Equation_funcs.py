from sympy import symbols,Eq, solve, sympify
from Basic_funcs import expr_convert, expr_convert_rev

def solve_eqn(equn, type):
    # try:
    if type == 1:
        return solve_poly(equn)
    elif type == 2:
        return solve_syst(equn)
    # except:
    #     return "MATH ERROR"

def substitute(expr, var, val):
    val = str(val)
    while var in expr:
        expr = expr.replace(var, val)
    
    expr = expr_convert(expr)
    try:
        return eval(expr)
    except NameError:
        return expr
    
def solve_poly(equn):
    x, y, z = symbols('x y z')
    sol = solve(equn)
    for i,e in enumerate(sol):
        e = str(e)
        if "pi" in e:
            sol[i] = expr_convert_rev(e)
    return sol

def solve_syst(equns):
    x, y, z = symbols("x y z")
    equn  = []
    for i in equns.split(","):
        j = i.split("=")
        equn.append(Eq(sympify(j[0]), sympify(j[1])))
    sol = solve(equn, (x, y, z))
    
    return sol
    
