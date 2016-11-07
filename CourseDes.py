import webbrowser
import DesParse
from tkinter import *


class App:

    def __init__(self, master):
        self.master = master
        self.parser = DesParse.Parser()
        self.widgets()

    def widgets(self):

        major_entry_label = Label(self.master, text="Enter subject area name or abbreviation:")
        major_entry_label.pack()

        major_entry = Entry(self.master)
        major_entry.pack()


        course_keyword_label = Label(self.master, text="Enter keyword you want to search for:")
        course_keyword_label.pack()

        course_keyword = Entry(self.master)
        course_keyword.pack()

        key_list = Listbox(self.master, selectmode=SINGLE)
        key_list.pack()
        for key in DesParse.regex_dict:
            key_list.insert(END, key)

        search_course = Button(self.master, text="Search course",
                                    command=lambda: self.parser.print_course(self.parser.get_course(course_keyword.get(),
                                    input_key=key_list.get(key_list.curselection()), major=major_entry.get())))
        search_course.pack()

        open_des = Button(self.master, text="Open course description website",
                          command=lambda: self.parser.open_coursedes(major_entry.get()))
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




