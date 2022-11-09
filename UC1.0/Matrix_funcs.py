from tkinter import *
from ttkbootstrap import Style
from tkinter import ttk

def read_matrix(cells):
    cell_vals = []
    row = len(cells)
    col = len(cells[0])
    for i in range(0, row):
        r = []
        for j in range(0, col):
            try:
                r.append(int(cells[i][j].get()))
            except ValueError:
                r.append(None)
        cell_vals.append(r)
    return cell_vals

def create_matrix(row, col, master):
    cells = []
    for i in range(0, row):
        r = []
        frame = ttk.Frame(master)
        frame.pack(pady=2)
        for j in range(0, col):
            disp =Entry(
                master             = frame,
                font               = ("Helvetica", "10"),
                justify            = LEFT,
                cursor             = "xterm",
                highlightcolor     = "#000000",
                highlightthickness = 3,
                bg                 = "white",
                relief             = GROOVE,
                width              = 5
            )
            disp.pack(side="left")
            r.append(disp)
        cells.append(r)
    return cells
