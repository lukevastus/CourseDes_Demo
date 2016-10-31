import webbrowser
import re
import DesParse
from tkinter import *


class App:

    def __init__(self, master):
        self.master = master
        self.parser = DesParse.Parser()
        self.widgets()

    def widgets(self):

        label = Label(self.master, text="Enter subject area name or abbreviation:")
        label.pack()

        entry = Entry(self.master)
        entry.pack()

        open_des = Button(self.master, text="Open course description website",
                          command=lambda: self.parser.open_coursedes(entry.get()))
        open_des.pack(fill=X)

        open_myucla = Button(self.master, text="MyUCLA", command=lambda: webbrowser.open("https://my.ucla.edu/"))
        open_myucla.pack(side=LEFT, fill=X)

        open_ccle = Button(self.master, text="CCLE", command=lambda: webbrowser.open("https://ccle.ucla.edu/"))
        open_ccle.pack(side=LEFT, fill=X)

        open_binf = Button(self.master, text="BINF worksheet",
                           command=lambda: webbrowser.open("http://www.seasoasa.ucla.edu/"
                                                           "wp-content/uploads/"
                                                           "seasoasa/Bioinformatics.pdf"))
        open_binf.pack(side=LEFT, fill=X)



