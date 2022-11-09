from string import ascii_uppercase, ascii_lowercase, digits

def update_base_disp(disp, disps, num, base, END, INSERT):
    result = base_conversion(num, base)

    if type(result) == str:
        disp.delete(0, END)
        disp.insert(disp.index(INSERT), result) 
        
        for i in range(len(disps)):
            disps[i].delete(0, END)
    else:
        for i in range(len(disps)):
            disps[i].delete(0, END)
            disps[i].insert(disps[i].index(INSERT), result[i]) 
        

def base_conversion(num, base):
    """Convert any numbers with base 2, 8, 10, 16, 32, 64 into the same

    Args:
        num (str): Value to be converted
        base (int): Input base value

    Returns:
        List: List of strings of binary, octal, decimal, hexadecimal, base 32 and base 64
    """    
    
    try:
        SYMBOLS = digits+ascii_uppercase+ascii_lowercase+"+/"
        
        sym = SYMBOLS[:base]
        dec = conv_dec(num, base, sym)
        
        bin = conv_base(dec, 2, SYMBOLS[:2])
        oct = conv_base(dec, 8, SYMBOLS[:8])
        hex = conv_base(dec, 16, SYMBOLS[:16])
        
        b_32 = conv_base(dec, 32, SYMBOLS[:32])
        b_64 = conv_base(dec, 64, SYMBOLS[:64])
        
        return [bin, oct, str(dec), hex, b_32, b_64]

    except:
        return "INVALID BASE NOTATION"
    
    
def conv_dec(num, base, sym):
    
    dec = 0
    
    for i, ele in enumerate(num[::-1]):
        dig = sym.index(ele)*(base**i)
        dec += dig
    
    return dec


def conv_base(dec, base, sym):
    
    ans = ""
    
    while dec > 0:
        ans = sym[dec%base] + ans 
        dec //= base
        
    return ans
    


