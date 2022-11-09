
# ~ Imports

from tkinter import *
from ttkbootstrap import Style
from tkinter import ttk
from tktooltip import ToolTip
from pyautogui import press

from math import *
from Basic_funcs import *
from Base_funcs import *
from Calculus_funcs import *
from Matrix_funcs import *
from Statistics_funcs import *
from Equation_funcs import *


# ~ Initial Variables

prev_ans = 0
root   = Tk()

ERRORS    = ["MATH ERROR", "INVALID BASE NOTATION"]
CONSTANTS = ["π", "e"]
BLACK     = "#000000"
WHITE     = "#FFFFFF"

root.geometry("800x500+300+300")
root.maxsize(800, 500)
root.minsize(650, 500)
root.iconbitmap("UC.ico")
root.config(cursor="@cur1054.cur")
root.title("Ultimate Calculator")

style = Style(theme = "cyborg")

def focus_next(next, *args):
    next.focus()
    
def input_here(here, text, *args):
    here.focus()
    if here == disp:
        if disp.get() in ERRORS:
            disp.delete(0, END)
    here.insert(here.index(INSERT), text)

# ~ Classes

class Calc_Buttons: 
    """A Class to create buttons on the Calculator Tab

        Args:
            master (Frame): Frame object created by tk.Frame() method.
            text (str): Text to be displayed on the button
            operate (str): Whether the button operates in ["Input","Output"]
            hover_text (srt): Text to be displayed on hover (setNone if not required)
            input_text (str, optional): Text to be inserted in disp if the button is pressed. Defaults to '' (Empty str).
            font (str, optional): The font style, size and etc. about the Text to be displayed on the button. Defaults to "Consolas 15".
            width (str, optional): Width of the Button.
            padx (str, optional): No of pixels Button to be padded along x axis.
            pady (str, optional): No of pixels Button to be padded along y axis.
            keys_to_press (list, optional): Keys to be pressed using pyautogui after the Text is inserted in disp if the button is pressed. Defaults to [] (Empty List).
        """
    def __init__(
        self,
        master,
        text,
        operate       = None,
        hover_text    = None,
        input_text    = "",
        font          = "Helvetica 15",
        width         = 1,
        padx          = 0,
        pady          = 0,
        command       = None,
        side          = LEFT,
        expand        = TRUE,
        fill          = BOTH,
        keys_to_press = []
        
    ):
        if command == None:
            command = self.clicked

        self.operate       = operate
        self.keys_to_press = keys_to_press
        self.input_text    = input_text
        self.btn           = Button(
            master,
            text      = text,
            font      = font,
            relief    = GROOVE,
            width     = width,
            command   = command,
            takefocus = False
        )
        
        if (hover_text != None):
            ToolTip(self.btn, msg = hover_text, delay = 0.5, follow = False)

        self.btn.pack(side = side, expand = expand, fill = fill, padx = padx, pady = pady)
        
    def clicked(self, *args):
        if self.operate == "Input":
            disp.focus()
            if self.input_text == "Clear":
                disp.delete(0, END)
            
            elif self.input_text == "Backspace":
                pos     = len(disp.get())
                display = str(disp.get())
                if display == "MATH ERROR":
                    disp.delete(0, END)
                    disp.insert(0, "0")
                else:
                    disp.delete(0, END)
                    disp.insert(0, display[0 : pos - 1])
            
            elif self.input_text == "Ans":
                if disp.get() in ERRORS:
                    disp.delete(0, END)
                disp.insert(disp.index(INSERT),"Ans")
                
            else:
                if disp.get() in ERRORS:
                    disp.delete(0, END)
                    disp.insert(disp.index(INSERT), self.input_text)
                    if self.keys_to_press != []:  
                        press(self.keys_to_press)
                
                else: 
                    try:  
                        val = disp.get().strip()
                        if val not in CONSTANTS:
                            float(val)

                        cond1 = [self.input_text == "()^2"]
                        
                        cond2 = ["(" in self.input_text, self.input_text not in ("^()", "*10^()")]
                        
                        if all(cond1):
                            disp.insert(disp.index(INSERT), "^2")
                        
                        elif all(cond2):
                            disp.delete(0, END)
                            disp.insert(disp.index(INSERT), self.input_text)
                            if self.keys_to_press != []:
                                press(self.keys_to_press)
                            disp.insert(disp.index(INSERT)-1, val)
                        else:
                            raise ValueError
                                
                    except ValueError:  
                        disp.insert(disp.index(INSERT), self.input_text)
            
                        if self.keys_to_press != []:
                            press(self.keys_to_press)
                
        
        elif self.operate == "Output":
            global ans, prev_ans
            if self.input_text == "round":
                try:
                    expr = eval(disp.get())
                    ans = round(float((expr)))
                    
                except Exception:
                    disp.delete(0, END)
                    disp.insert(disp.index(INSERT), "MATH ERROR") 
                    
            elif self.input_text == "Equal to":
                ans = "MATH ERROR"
                try:
                    expr = str(disp.get())
                    expr = expr_convert(expr, prev_ans)
    
                    ans = eval(expr)
                    
                    prev_ans = ans
                    
                    if int(ans) == ans:
                        ans = int(ans)
                
                except:
                    disp.delete(0, END)
                    disp.insert(disp.index(INSERT), "MATH ERROR") 
                print(f"{expr} = {ans}")
            
            elif self.input_text == "dec_frac":
                expr = disp.get()
                n,d = float_to_fraction(eval(expr_convert(expr)))
                ans = str(n)+"/"+str(d)
            
            elif self.input_text == "dec_mixfrac":
                expr = disp.get()
                f,n,d = float_to_mixfarction(eval(expr_convert(expr)))
                ans = f"{f}[{n}/{d}]"
            
            ans = str(ans)
            ans = ans.replace("e", "*10^")
            disp.delete(0, END)
            disp.insert(0, ans)

# ~ Functions

def key_event(*args):
    if disp.get() == "0":
        disp.delete(0, END)

def dot_btn_clicked():
    disp.insert(disp.index(INSERT), "․")
    
def update_display(disp, msg):
    disp.delete(0, END)
    if type(msg) == list and type(msg[0]) == str:
        s = "" + msg[0]
        for i in msg[1:]:
            s += ", " + str(i)
        msg = s
    disp.insert(disp.index(INSERT), str(msg))

# ~ Entry box [disp] - Common for all Tabs

disp = Entry(
    root,
    font               = ("Helvetica", "20"),
    justify            = RIGHT,
    cursor             = "xterm",
    highlightcolor     = BLACK,
    highlightthickness = 3,
    bg                 = "white",
    relief             = GROOVE,
)
disp.pack(expand = TRUE, fill = BOTH)


# ~ Notebook Tabs

ttk.Style().configure("TNotebook", background = BLACK, foreground = "white")

TC   = ttk.Notebook(root)
tab1 = ttk.Frame(TC)
tab2 = ttk.Frame(TC)
tab3 = ttk.Frame(TC)
tab4 = ttk.Frame(TC)
tab5 = ttk.Frame(TC)


TC.add(tab1, text =  "Standard")
TC.add(tab2, text =  "Statistics")
TC.add(tab3, text =  "Base N")
TC.add(tab4, text =  "Equations")
TC.add(tab5, text =  "Calculus")

TC.pack(expand = 1, fill = "both")

#~ Calculator Tab

btn_row_1 = ttk.Frame(tab1)
btn_row_1.pack(expand = TRUE, fill = BOTH)

pi_btn = Calc_Buttons(
    master = btn_row_1, 
    text = "π", 
    operate = "Input", 
    input_text =  "π",
    hover_text = "Pi"
)

fact_btn = Calc_Buttons(
    master        = btn_row_1,
    text          = " x! ",
    operate       = "Input",
    input_text    = "fact()",
    keys_to_press = ["left"],
    hover_text    = "Factorial"
)

round_btn = Calc_Buttons(
    master     = btn_row_1,
    text       = "⌊x⌋",
    operate    = "Output",
    input_text = "round",
    font       = "Consolas 15 bold",
    hover_text = "Round off"
)

sin_btn = Calc_Buttons(
    master        = btn_row_1,
    text          = "  sin   ",
    operate       = "Input",
    input_text    = "sin()",
    keys_to_press = ["left"],
    hover_text    = "Sine"
)

cos_btn = Calc_Buttons(
    master        = btn_row_1,
    text          = "  cos   ",
    operate       = "Input",
    input_text    = "cos()",
    keys_to_press = ["left"],
    hover_text    = "Cosine"
)

tan_btn = Calc_Buttons(
    master        = btn_row_1,
    text          = "  tan   ",
    operate       = "Input",
    input_text    = "tan()",
    keys_to_press = ["left"],
    hover_text    = "Tangent"
)

btn_1 = Calc_Buttons(
    master =  btn_row_1, text =  "1", operate =  "Input",  input_text =  "1",
    hover_text = None
)

btn_2 = Calc_Buttons(
    master =  btn_row_1, text =  "2", operate =  "Input",  input_text =  "2",
    hover_text = None
)

btn_3 = Calc_Buttons(
    master =  btn_row_1, text =  "3", operate =  "Input",  input_text =  "3",
    hover_text = None
)

btn_plus = Calc_Buttons(
    master     = btn_row_1,
    text       = "+",
    operate    = "Input",
    input_text = "+",
    font       = "Consolas 15 bold",
    hover_text = "Addition"
)


# ~ Row 2 Buttons

btn_row_2 = ttk.Frame(tab1)
btn_row_2.pack(expand = TRUE, fill = BOTH)

e_btn = Calc_Buttons(
    master =  btn_row_2, text =  "e", operate =  "Input", input_text =  "e",
    hover_text = "Euler's Number"
)

sqrt_btn = Calc_Buttons(
    master        = btn_row_2,
    text          = " √x ",
    operate       = "Input",
    input_text    = "√()",
    keys_to_press = ["left"],
    hover_text    = "Square Root"
)

nth_rt_btn = Calc_Buttons(
    master        = btn_row_2,
    text          = " n√x ",
    operate       = "Input",
    input_text    = "n√()",
    keys_to_press = ["left"],
    hover_text    = "nth Root"
)

csc_btn = Calc_Buttons(
    master        = btn_row_2,
    text          = "  csc   ",
    operate       = "Input",
    input_text    = "csc()",
    keys_to_press = ["left"],
    hover_text    = "Cosecant"
)

sec_btn = Calc_Buttons(
    master        = btn_row_2,
    text          = "  sec   ",
    operate       = "Input",
    input_text    = "sec()",
    keys_to_press = ["left"],
    hover_text    = "Secant"
)

cot_btn = Calc_Buttons(
    master        = btn_row_2,
    text          = "  cot   ",
    operate       = "Input",
    input_text    = "cot()",
    keys_to_press = ["left"],
    hover_text    = "Cotangent"
)

btn_4 = Calc_Buttons(
    master =  btn_row_2, text =  "4", operate =  "Input",  input_text =  "4",
    hover_text = None
)
btn_5 = Calc_Buttons(
    master =  btn_row_2, text =  "5", operate =  "Input",  input_text =  "5",
    hover_text = None
)
btn_6 = Calc_Buttons(
    master =  btn_row_2, text =  "6", operate =  "Input",  input_text =  "6",
    hover_text = None
)

btn_minus = Calc_Buttons(
    master     = btn_row_2,
    text       = "-",
    operate    = "Input",
    input_text = "-",
    font       = "Consolas 15 bold",
    hover_text = "Subtraction"
)

# ~ Row 3 Buttons

btn_row_3 = ttk.Frame(tab1)
btn_row_3.pack(expand = TRUE, fill = BOTH)

dec_frac_btn = Calc_Buttons(
    master     = btn_row_3,
    text       = " D⇔F ",
    operate    = "Output",
    input_text = "dec_frac",
    font       = "Consolas 12 bold",
    hover_text = "Decimal to Fraction"
)

sqr_btn = Calc_Buttons(
    master        = btn_row_3,
    text          = " x² ",
    operate       = "Input",
    input_text    = "()^2",
    keys_to_press = ["left", "left", "left"],
    hover_text    = "Square"
)

pow_btn = Calc_Buttons(
    master =  btn_row_3, 
    text =  "x\u02B8", 
    operate =  "Input", 
    input_text =  "^()", 
    keys_to_press = ["left"],
    hover_text    = "x Power y"
)

sini_btn = Calc_Buttons(
    master        = btn_row_3,
    text          = "sin\u207B\u00B9",
    operate       = "Input",
    input_text    = "sin\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Sine Inverse"
)

cosi_btn = Calc_Buttons(
    master        = btn_row_3,
    text          = "cos\u207B\u00B9",
    operate       = "Input",
    input_text    = "cos\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Cosine Inverse"
)

tani_btn = Calc_Buttons(
    master        = btn_row_3,
    text          = "tan\u207B\u00B9",
    operate       = "Input",
    input_text    = "tan\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Tangent Inverse"
)

btn_7 = Calc_Buttons(
    master =  btn_row_3, text =  "7", operate =  "Input",  input_text =  "7",
    hover_text = None
)

btn_8 = Calc_Buttons(
    master =  btn_row_3, text =  "8", operate =  "Input",  input_text =  "8",hover_text = None
)

btn_9 = Calc_Buttons(
    master =  btn_row_3, text =  "9", operate =  "Input",  input_text =  "9",
    hover_text = None
)

btn_mul = Calc_Buttons(
    master     = btn_row_3,
    text       = "*",
    operate    = "Input",
    input_text = "*",
    font       = "Consolas 15 bold",
    hover_text = "Multiplication"
)

# ~ Row 4 Buttons

btn_row_4 = ttk.Frame(tab1)
btn_row_4.pack(expand = TRUE, fill = BOTH)

dec_mixfrac_btn =  Calc_Buttons(
    master     = btn_row_4,
    text       = " D⇔MF",
    operate    = "Output",
    input_text = "dec_mixfrac",
    font       = "Consolas 12 bold",
    hover_text = "Decimal to Mixed-Fraction"
)

bo_btn = Calc_Buttons(
    master        = btn_row_4,
    text          = "(",
    operate       = "Input",
    input_text    = "()",
    keys_to_press = ["left"],
    hover_text    = None
)

bc_btn = Calc_Buttons(
    master =  btn_row_4, text =  ")", operate =  "Input",  input_text =  ")",
    hover_text = None
)

csci_btn = Calc_Buttons(
    master        = btn_row_4,
    text          = "csc\u207B\u00B9",
    operate       = "Input",
    input_text    = "csc\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Cosecant Inverse"
)

seci_btn = Calc_Buttons(
    master        = btn_row_4,
    text          = "sec\u207B\u00B9",
    operate       = "Input",
    input_text    = "sec\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Secant Inverse"
)

coti_btn = Calc_Buttons(
    master        = btn_row_4,
    text          = "cot\u207B\u00B9",
    operate       = "Input",
    input_text    = "cot\u207B\u00B9()",
    keys_to_press = ["left"],
    hover_text    = "Cotangent Inverse"
)

dot_btn = Calc_Buttons(
    master =  btn_row_4, text =  " • ", operate =  "Input",  input_text =  ".",
    hover_text = None
)

btn_0 = Calc_Buttons(
    master =  btn_row_4, text =  "0", operate =  "Input",  input_text =  "0",
    hover_text = "0"
)

btn_eq = Calc_Buttons(
    master     = btn_row_4,
    text       = "=",
    operate    = "Output",
    font       = "Consolas 15 bold",
    input_text = "Equal to",
    hover_text = "Calculate"
)

btn_div = Calc_Buttons(
    master     = btn_row_4,
    text       = "÷",
    operate    = "Input",
    input_text = "/",
    font       = "Consolas 15 bold",
    hover_text = "Division"
)

# ~ Row 5 Buttons

btn_row_5 = ttk.Frame(tab1)
btn_row_5.pack(expand = TRUE, fill = BOTH)

Ans_btn = Calc_Buttons(
    master =  btn_row_5, text =  "Ans", operate =  "Input",  input_text =  "Ans",
    hover_text = "Previous Answer"
)

ten_pwr = Calc_Buttons(
    master        = btn_row_5,
    text          = "*10ⁿ",
    operate       = "Input",
    input_text    = "*10^()",
    keys_to_press = ["left"],
    hover_text    = "*10 Power"
)
    
ln_btn = Calc_Buttons(
    master        = btn_row_5,
    text          = "ln",
    operate       = "Input",
    input_text    = "ln()",
    keys_to_press = ["left"],
    hover_text    = "Natural log"
)

log10_btn = Calc_Buttons(
    master        = btn_row_5,
    text          = "log10",
    operate       = "Input",
    input_text    = "log10()",
    keys_to_press = ["left"],
    hover_text    = "log base 10"
)

logn_btn = Calc_Buttons(
    master        = btn_row_5,
    text          = "logₙ",
    operate       = "Input",
    input_text    = "logn()",
    keys_to_press = ["left", "left"],
    hover_text    = "log base n"
)

nPr_btn = Calc_Buttons(
    master        = btn_row_5,
    text          = "\u207FP\u1D63",
    operate       = "Input",
    input_text    = "P",
    hover_text    = "Permutation"
)

nCr_btn = Calc_Buttons(
    master        = btn_row_5,
    text          = "\u207FC\u1D63",
    operate       = "Input",
    input_text    = "C",
    hover_text    = "Combination"
)

del_btn = Calc_Buttons(
    master     = btn_row_5,
    text       = "⌫",
    operate    = "Input",
    input_text = "Backspace",
    hover_text = "Backspace"
)

btn_c = Calc_Buttons(
    master     = btn_row_5,
    text       = "C",
    operate    = "Input",
    input_text = "Clear",
    hover_text = "Clear"
)

rem_btn = Calc_Buttons(
    master     = btn_row_5,
    text       = "%",
    operate    = "Input",
    input_text = "%",
    hover_text = "Remainder"
)

# ~ Equations Tab

row1 = ttk.Frame(tab4)
row1.pack(pady = 10)

l1 = ttk.Label(text = "Substitute ", master = row1, font = "Helvetica 12")
l1.pack(side = "left")

val = ttk.Entry(master = row1, width = 4)
val.pack(side = "left")

l1 = ttk.Label(text =" for ", master = row1, font = "Helvetica 12")
l1.pack(side = "left")

var = ttk.Entry(master = row1, width = 4)
var.pack(side = "left")

compute = Calc_Buttons(
    master     = row1,
    text       = "Compute",
    operate    = "Output",
    font       = "Helvetica",
    width      = 10,
    padx       = 10,
    hover_text = None,
    command    = lambda : update_display(disp, substitute(disp.get(), var.get(), val.get()))
)

val.bind("<Return>", lambda event, next = var : focus_next(next))

row2 = ttk.Frame(tab4)
row2.pack()

equn_type = IntVar()

r1 = ttk.Radiobutton(
    master   = row2,
    text     = "Polynomial Equation",
    value    = 1,
    variable = equn_type
)
r1.pack(side = "left")

r2 = ttk.Radiobutton(
    master   = row2,
    text     = "System of Equations",
    value    = 2,
    variable = equn_type
)
r2.pack(side = "left", padx = 10)

solve = Calc_Buttons(
    master     = row2,
    text       = "Solve",
    operate    = "Output",
    font       = "Helvetica",
    width      = 10,
    padx       = 10,
    hover_text = None,
    command    = lambda : update_display(disp, solve_eqn(disp.get(), equn_type.get()))
) 

row4 = ttk.Frame(tab4)
row4.pack(pady= 15)

btn_x = Button(
    master = row4,
    text = "X",
    font    = "Helvetica",
    width   = 5,
    command = lambda : input_here(root.focus_get(), "x")
)

btn_x.pack(padx = 5,
    expand = True,
    fill = BOTH, 
    side = LEFT
)

btn_y = Button(
    master = row4,
    text = "Y",
    font    = "Helvetica",
    width   = 5,
    command = lambda : input_here(root.focus_get(), "y")
)

btn_y.pack(padx = 5,
    expand = True,
    fill = BOTH,
    side = LEFT
)

btn_z = Button(
    master = row4,
    text = "Z",
    font    = "Helvetica",
    width   = 5,
    command = lambda : input_here(root.focus_get(), "z")
)

btn_z.pack(padx = 5,
    expand = True,
    fill = BOTH,
    side = LEFT
)

btn_comma = Button(
    master = row4,
    text = ",",
    font    = "Helvetica",
    width   = 5,
    command = lambda : input_here(disp, ", ")
)

btn_comma.pack(padx = 5,
    expand = True,
    fill = BOTH,
    side = LEFT
)

btn_equal = Button(
    master = row4,
    text = "=",
    font    = "Helvetica",
    width   = 5,
    command = lambda : input_here(disp, " = ")
)

btn_equal.pack(padx = 5,
    expand = True,
    fill = BOTH,
    side = LEFT
)

row5 = ttk.Frame(tab4)
row5.pack(fill= BOTH)

l1 = ttk.Label(text = "Note : Separate the System of Equations using comma(,) ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 8)

row6 = ttk.Frame(tab4)
row6.pack(fill= BOTH)

l1 = ttk.Label(text = "          Do not Equate Polynomial Equations to any Value ", master = row6, font = "Helvetica 12")
l1.pack(side = "left", padx = 8)

# ~ Calculus Tab

row1 = ttk.Frame(tab5)
row1.pack(expand = True)

l1 = ttk.Label(text = "Note : Please use only x as the Variable ", master = row1, font = "Helvetica 12")
l1.pack(side = "left", padx = 5, pady = 5)

row2 = ttk.Frame(tab5, width=30)
row2.pack(expand = True, fill = BOTH, anchor = CENTER)

fod_btn = Calc_Buttons(
    master     = row2,
    text       = "F'(x)",
    font       = "Helvetica",
    hover_text = "First order differentiation",
    command    = lambda : update_display(disp, differentation(disp.get()))
)

intg_btn = Calc_Buttons(
    master     = row2,
    text       = "ʃ F(x)",
    font       = "Helvetica",
    hover_text = "Integral",
    command    = lambda : update_display(disp, integration(disp.get()))
)

row3 = ttk.Frame(tab5)
row3.pack(expand = True,fill = BOTH, anchor = CENTER)

sod_btn = Calc_Buttons(
    master     = row3,
    text       = "F\"(x)",
    font       = "Helvetica",
    hover_text = "First order differentiation",
    command    = lambda : update_display(disp, differentation(disp.get(), 2))
)

intg_ab_btn = Calc_Buttons(
    master     = row3,
    text       = "ₐʃᵇ F(x)",
    font       = "Helvetica",
    hover_text = "Integral a to b",
    command    = lambda : update_display(disp, integration_limits(disp.get(), e_a.get(), e_b.get()))
)

row4 = ttk.Frame(tab5)
row4.pack(expand = True, fill = BOTH, anchor = CENTER)

nod_btn = Calc_Buttons(
    master     = row4,
    text       = "Fⁿ(x)",
    font       = "Helvetica",
    hover_text = "nth order differentiation",
    command    = lambda : update_display(disp, differentation(disp.get(), e_n.get()))
)

row5 = ttk.Frame(tab5)
row5.pack(expand = True, fill = BOTH, anchor = CENTER)

l1 = ttk.Label(text = "n : ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_n = Entry(
            master             = row5,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 5 
        )

e_n.pack(side="left")

l1 = ttk.Label(text = "a : ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_a = Entry(
            master             = row5,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 5 
        )

e_a.pack(side="left")

l1 = ttk.Label(text = "b : ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_b = Entry(
            master             = row5,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 5 
        )

e_b.pack(side="left")

e_a.bind("<Return>", lambda event, next = e_b : focus_next(next))
e_b.bind("<Return>", lambda event, next = e_a : focus_next(next))

# ~ Base N Tab

row1 = ttk.Frame(tab3)
row1.pack(pady = 10, anchor = "w")

l1 = ttk.Label(text = "Input : ", master = row1, font = "Helvetica 12")
l1.pack(side = "left", padx = 5)

base = IntVar()

r_base_2 = ttk.Radiobutton(
    master   = row1,
    text     = "Binary",
    value    = 2,
    variable = base
)

r_base_2.pack(side = "left", padx = 5)

r_base_8 = ttk.Radiobutton(
    master   = row1,
    text     = "Octal",
    value    = 8,
    variable = base
)

r_base_8.pack(side = "left", padx = 5)

r_base_10 = ttk.Radiobutton(
    master   = row1,
    text     = "Decimal",
    value    = 10,
    variable = base
)

r_base_10.pack(side = "left", padx = 5)

r_base_16 = ttk.Radiobutton(
    master   = row1,
    text     = "Hexa-Decimal",
    value    = 16,
    variable = base
)

r_base_16.pack(side = "left", padx = 5)

r_base_32 = ttk.Radiobutton(
    master   = row1,
    text     = "Base 32",
    value    = 32,
    variable = base
)

r_base_32.pack(side = "left", padx = 5)

r_base_64 = ttk.Radiobutton(
    master   = row1,
    text     = "Base 64",
    value    = 64,
    variable = base
)

r_base_64.pack(side = "left", padx = 5)

row2 = ttk.Frame(tab3)
row2.pack(pady = 10, anchor = "w")

l1 = ttk.Label(text = "Output : ", master = row2, font = "Helvetica 12")
l1.pack(padx = 5)

row3 = ttk.Frame(tab3)
row3.pack(pady = 10, anchor = "w")

l1 = ttk.Label(text = "Binary     : ", master = row3, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base2 = Entry(
            master             = row3,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base2.pack(side="left")

l1 = ttk.Label(text = "Octal             : ", master = row3, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base8 = Entry(
            master             = row3,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base8.pack(side="left")

row4 = ttk.Frame(tab3)
row4.pack(pady = 10, anchor = "w")

l1 = ttk.Label(text = "Decimal  : ", master = row4, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base10 = Entry(
            master             = row4,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base10.pack(side="left")

l1 = ttk.Label(text = "Hexa-Decimal  : ", master = row4, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base16 = Entry(
            master             = row4,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base16.pack(side="left")

row5 = ttk.Frame(tab3)
row5.pack(pady = 10, anchor = "w")

l1 = ttk.Label(text = "Base-32  : ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base32 = Entry(
            master             = row5,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base32.pack(side="left")

l1 = ttk.Label(text = "Base-64          : ", master = row5, font = "Helvetica 12")
l1.pack(side = "left", padx = 20)

e_base64 = Entry(
            master             = row5,
            font               = ("Helvetica", "16"),
            justify            = LEFT,
            cursor             = "xterm",
            highlightcolor     = BLACK,
            highlightthickness = 3,
            bg                 = "white",
            relief             = GROOVE,
            width              = 10 
        )

e_base64.pack(side="left")

disps = [e_base2, e_base8, e_base10,
         e_base16, e_base32, e_base64]

row6 = ttk.Frame(tab3)
row6.pack(pady = 5) 

compute = Button(
    master     = row6,
    text       = "Compute",
    font       = "Helvetica",
    width      = 10,
    padx       = 10,
    command    = lambda : update_base_disp(disp, disps, disp.get(), base.get(), END, INSERT)
)

compute.pack()

# ~ Statistics Tab

data_frame = Frame(tab2)
data_frame.pack(side = "left", anchor="w", padx = 20)

l1 = ttk.Label(text = "Data Values", master = data_frame, font = "Helvetica 12")
l1.pack(padx = 3)

data_cells = create_matrix(10, 1, data_frame)

for i, e in enumerate(data_cells[0:len(data_cells)-1]):
    e[0].bind("<Return>", lambda event, next = data_cells[i+1][0] : focus_next(next))

data_cells[len(data_cells)-1][0].bind("<Return>", lambda event, next = data_cells[0][0] : focus_next(next))

btn_frame = Frame(tab2)
btn_frame.pack(fill=BOTH, expand=True, padx = 50, pady= 15)

row1 = Frame(btn_frame)
row1.pack(fill = BOTH, expand=True)

mean_btn = Calc_Buttons(
    master     = row1,
    text       = "Mean",
    font       = "Helvetica",
    hover_text = "Mean",
    command    = lambda : update_display(disp, mean([i[0] for i in read_matrix(data_cells)]))
)

median_btn = Calc_Buttons(
    master     = row1,
    text       = "Median",
    font       = "Helvetica",
    hover_text = "Median",
    command    = lambda : update_display(disp, median([i[0] for i in read_matrix(data_cells)])),
    
)

mode_btn = Calc_Buttons(
    master     = row1,
    text       = "Mode",
    font       = "Helvetica",
    hover_text = "Mode",
    command    = lambda : update_display(disp, mode([i[0] for i in read_matrix(data_cells)]))
)

row2 = Frame(btn_frame)
row2.pack(fill = BOTH, expand=True)

total_btn = Calc_Buttons(
    master     = row2,
    text       = "Sum",
    font       = "Helvetica",
    hover_text = "Sum of all Data",
    command    = lambda : update_display(disp, sum(clense_data([i[0] for i in read_matrix(data_cells)])))
)

range_btn = Calc_Buttons(
    master     = row2,
    text       = "Range",
    font       = "Helvetica",
    hover_text = "Range",
    command    = lambda : update_display(disp, range([i[0] for i in read_matrix(data_cells)]))
)

iqr_btn = Calc_Buttons(
    master     = row2,
    text       = "IQR",
    font       = "Helvetica",
    hover_text = "Inter Quartile Range",
    command    = lambda : update_display(disp, iqr([i[0] for i in read_matrix(data_cells)]))
)

row3 = Frame(btn_frame)
row3.pack(fill = BOTH, expand=True)

SS_btn = Calc_Buttons(
    master     = row3,
    text       = "SS",
    font       = "Helvetica",
    hover_text = "Sum of Squares from Mean",
    command    = lambda : update_display(disp, sum_of_squares([i[0] for i in read_matrix(data_cells)]))
)

variance_btn = Calc_Buttons(
    master     = row3,
    text       = "Variance",
    font       = "Helvetica",
    hover_text = "Variance",
    command    = lambda : update_display(disp, variance([i[0] for i in read_matrix(data_cells)]))
)

sd_btn = Calc_Buttons(
    master     = row3,
    text       = "Std dev",
    font       = "Helvetica",
    hover_text = "Standard Deviation",
    command    = lambda : update_display(disp, std_dev([i[0] for i in read_matrix(data_cells)]))
)

# ~ Binding Keys

#> Bind function passes some arguments to the called function, so use *args in the function

disp.bind("<Return>", btn_eq.clicked) 
disp.bind("<Escape>", btn_c.clicked)
disp.bind("<Key-1>", key_event)
disp.bind("<Key-2>", key_event)
disp.bind("<Key-3>", key_event)
disp.bind("<Key-4>", key_event)
disp.bind("<Key-5>", key_event)
disp.bind("<Key-6>", key_event)
disp.bind("<Key-7>", key_event)
disp.bind("<Key-8>", key_event)
disp.bind("<Key-9>", key_event)
disp.bind("<Key-0>", key_event)
disp.bind("<Key-.>", dot_btn_clicked)

disp.focus()

root.mainloop()