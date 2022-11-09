from math import floor
from regex import findall 

# ~ Expression Conversion Function

def expr_convert(expr, prev_ans = 0):
                
    opr = [("π","pi"),
           ("^","**"),
           ("fact(","factorial("),
           ("csc(", "1/sin("),
           ("sec(", "1/cos("),
           ("cot(", "1/tan("),
           ("sin⁻¹(","asin("),
           ("cos⁻¹(","acos("),
           ("tan⁻¹(","atan("),
           ("csc⁻¹(","1/asin("),
           ("sec⁻¹(","1/acos("),
           ("cot⁻¹(","atan("),
           ("ln(","log("),
           ("Ans", str(prev_ans))]

    for x in opr:
        if x[0] in expr:
            expr = expr.replace(x[0], x[1])
            
    expr = n_and_r(expr, "P", "perm")
    expr = n_and_r(expr, "C", "comb")
    expr = conv_roots(expr)
    
    expr = expr.replace("√(", "sqrt(")
    
    if "log" in expr:
        f = findall("log[0-9]+\([0-9]+\)", expr)
        
        for i in f:
            arr = findall("[0-9]+", i)
            base = arr[0]
            num = arr[1]
            
            expr = expr.replace(i, "(log("+num+")/log("+base+"))")
    
    if "[" in expr:
        f = findall("\d+\[\d+/\d+\]", expr)
    
        for i in f:
            front = int(i[0:i.index("[")])
            num   = int(i[i.index("[")+1:i.index("/")])
            den   = int(i[i.index("/")+1:-1])
            
            expr = expr.replace(i, f"{(front*den+1)/den}")
            
    return expr

def expr_convert_rev(expr, prev_ans = 0):
    opr = [("π","pi"),
           ("^","**"),
           ("fact(","factorial("),
           ("csc(", "1/sin("),
           ("sec(", "1/cos("),
           ("cot(", "1/tan("),
           ("sin⁻¹(","asin("),
           ("cos⁻¹(","acos("),
           ("tan⁻¹(","atan("),
           ("csc⁻¹(","1/asin("),
           ("sec⁻¹(","1/acos("),
           ("cot⁻¹(","atan("),
           ("ln(","log("),
           ("Ans", str(prev_ans))]

    for x in opr:
        if x[1] in expr:
            expr = expr.replace(x[1], x[0])
            
    return expr

def conv_roots(expr):
    while expr.count("√") > 0:
        f = findall("[0-9]+√\(.+", expr)
        for i in f:
            root = i[:i.index("√")]
            num = find_r(i, "√")
            expr = expr.replace(f"{root}√{num}", f"nth_root({root}, {num})")
        
        if f == []:
            break
    return expr
        
            
def n_and_r(expr, char, opr):
    
    while expr.count(char) > 0:
        
        perm = findall(f"[0-9]+{char}[0-9]+", expr)
    
        if perm != []:
            for i in perm:
                n, r = i.split(char)
                expr = expr.replace(i, f"{opr}({n}, {r})")
                
        perm = findall(f"[0-9]+{char}\(.+", expr)
        
        if perm != []:
            for i in perm:
                n, r = i.split(char)
                r = find_r(i, char)
                expr = expr.replace(i, f"{opr}({n}, {r})")

        perm = findall(f".+\){char}[0-9]+", expr)
        
        if perm != []:
            for i in perm:
                n, r = i.split(char)
                n = find_n(i, char)
                expr = expr.replace(i, f"{opr}({n}, {r})")

        perm = findall(f".+\){char}\(.+", expr)
    
        if perm != []:
            for i in perm:
                n = find_n(i, char)
                r = find_r(i, char)
                s = expr[expr.find(n):expr.find(r)+len(r)]
                expr = expr.replace(s, f"{opr}({n}, {r})")
        
    return (expr)

def fact(n):

    if n == 1:
        return 1
    elif n == 0:
        return 1
    if n<0:
        return "MATH ERROR"
    else:
        return n * fact(n - 1)
    
def perm(n, r):
    if r <= n:
        return fact(n) / fact(n - r)
    else:
        return "MATH ERROR"


def comb(n, r):
    if r <= n:
        return perm(n, r) / fact(r)
    else:
        return "MATH ERROR"

def find_n(expr, char):
    n = ""
    bc = 0
    for i in expr[expr.index(f"){char}")::-1]:
        if i == ")":
            bc += 1
        elif i == "(":
            bc -= 1
        n = i + n
        if bc == 0:
            break
    return (n)

def find_r(expr, char):

    r = ""
    bo = 0
    for i in expr[expr.index(f"{char}(")+1:]:
        
        if i == ")":
            bo -= 1
        elif i == "(":
            bo += 1
        r = r + i
    
        if bo == 0:
            break
    return (r)

def float_to_fraction(x, error=0.000001):
    #Stern-Brocot tree Algorithm
    n = int(floor(x))
    x -= n
    if x < error:
        return (n, 1)
    elif 1 - error < x:
        return (n + 1, 1)

    # The lower fraction is 0/1
    lower_n = 0
    lower_d = 1
    # The upper fraction is 1/1
    upper_n = 1
    upper_d = 1
    while True:
        # The middle fraction is (lower_n + upper_n) / (lower_d + upper_d)
        middle_n = lower_n + upper_n
        middle_d = lower_d + upper_d
        # If x + error < middle
        if middle_d * (x + error) < middle_n:
            # middle is our new upper
            upper_n = middle_n
            upper_d = middle_d
        # Else If middle < x - error
        elif middle_n < (x - error) * middle_d:
            # middle is our new lower
            lower_n = middle_n
            lower_d = middle_d
        # Else middle is our best fraction
        else:
            return (n * middle_d + middle_n, middle_d)

def float_to_mixfarction(x):
    num, den = float_to_fraction(x)
    front = num//den
    num = num % den
    return (front, num, den)

def nth_root(root, n):
    return n**(1/root)
    