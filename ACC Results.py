
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
import glob
import os
import _datetime as data
import Util_functions


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
    def state(self):
        return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
    root = Tk()
    root.geometry("450x90")
    root.resizable(False, False)
    root.title("ACC Statistics (By Vladi Kruk)")
    lng = Checkbar(root, ['Developer', 'Electroda',
                          'Density', 'Conductivity',
                          "Optical Density" ])
    lng.place(x=8,y=5)
    # tgl = Checkbar(root, ['English','German']).place(x=8,y=5)
    lng.config(relief=GROOVE, bd=2)

    # def ShowOnScreen():
    #     if ChackBoxIsEmpty():
    #         print(getACC_DataFrame())

    # file_frame = LabelFrame(root, text="Save To",width=60, padx=10, pady=4)
    # file_frame.grid(row= 1, column=1,columnspan=4)#pack(side=TOP)
    # #   Input field
    # file_path = Entry(file_frame, width=70, border=2)
    # file_path.insert(0,"")
    # file_path.grid(row=0, column=0)
    Button(root, text='Save', command=lambda: file_save(), width=10, padx=0, pady=8).place(width = 100,x=240,y=40)
    Button(root, text='Show', command=lambda: ShowOnScreen(), width=10, padx=0, pady=8).place(width = 100,x=110,y=40)
    root.mainloop()
