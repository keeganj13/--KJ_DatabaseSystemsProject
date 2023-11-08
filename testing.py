
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import numpy as np

def buildTree(columnNames, rows, parent, scrollBar=None, columnWidth=150, customHeight=6):
    if scrollBar is not None:
        T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=customHeight, padding=5, yscrollcommand=scrollBar.set)
    else:
        T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=customHeight, padding=5)
    for i in range(len(columnNames)):
        T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
        T.heading('# '+str(i+1), text=columnNames[i])
    for row in [list(r) for r in rows]:
        T.insert('', tk.END, text=row, values=row)
    return T 

class GUI:
    def __init__(self, title='Window Title'):
        self.title = title
        self.window = tk.Tk()
        self.window.title(self.title)
    def show(self):
        self.window.mainloop()

class Function:
    '''Creates a Function object with a string as its equation'''
    def __init__(self, equation=''):
        self.equation = equation

    def eval(self, x=0):
        '''Evaluates the equation at the value x which is an int'''
        eq = [char for char in self.equation.replace(' ','')]
        for i in range(len(eq)):
            if 'x' in eq[i] and eq[i-1] not in '/+-*^()':
                eq[i] = '*x'
            elif '^' in eq[i]:
                eq[i] = '**'

        try:
            x=float(x)
            print(eq)
            return eval(''.join(eq))
        except Exception as e:
            return e

def main():
    Window = GUI('Main Window')

    EQFrm = tk.Frame(master=Window.window, padx=50, pady=10)
    EQFrm.pack()

    ttk.Label(master=EQFrm, text='Equation:').grid(column=0, row=0)
    EQTxt = tk.Text(master=EQFrm, height=1,width=50)
    EQTxt.grid(column=0,row=1)

    XValFrm = tk.Frame(master=Window.window, padx=50, pady=10)
    XValFrm.pack()

    ttk.Label(master=XValFrm, text='X Range:').grid(column=0, row=0)
    XValTxt = tk.Text(master=XValFrm, width=20, height=1)
    XValTxt.grid(column=0,row=1)

    btnFrm = tk.Frame(master=Window.window, padx=50, pady=10)
    btnFrm.pack()

    def showGraph(e = None):
        eq = EQTxt.get('1.0', 'end').strip()
        xVal = XValTxt.get('1.0', 'end').strip().split(',')
        print(eq, xVal)
        
        def f(x):
            return Function(eq).eval(x)
        
        xpoints = []
        ypoints = []
        for i in range(int(xVal[0]), int(xVal[1]+1)):
            print(i)
            ypoints += [f(i)]
            xpoints += [i]
        
        xpoints = np.array(xpoints)
        ypoints = np.array(ypoints)
        
        plt.plot(xpoints, ypoints)
        plt.show()

    ttk.Button(master=btnFrm, text='Show Graph', command=showGraph).pack()

    Window.show()

main()