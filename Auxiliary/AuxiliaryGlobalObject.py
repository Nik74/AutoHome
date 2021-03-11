# encoding: utf-8

import pyperclip
import gettext

from win32api import GetSystemMetrics
from tkinter import *
from tkinter import ttk
from Auxiliary import AuxiliaryFunctions as AF

# height and width of window
height_window = GetSystemMetrics(1)
width_window = GetSystemMetrics(0)

height_program = int(GetSystemMetrics(1) / 1.5)
width_program = int(GetSystemMetrics(0) / 2)

# object for translate message
t = gettext.translation('messages', './locale', languages=['ru'])
t.install()

_ = t.gettext

path_logo_ico = 'img/logo.ico'


# Class for Button
class CreateButton(Button):
    def __init__(self, master=None, text='', command=None, row=0, column=0, bg=None,
                 columnspan=1, sticky='ew'):
        super().__init__(master)
        self.config(text=text, bg=bg)

        if command is not None:
            self.config(command=command)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for Entry
class CreateEntry(Entry):
    def __init__(self, master=None, row=0, column=0, columnspan=1, sticky='ew', item='',
                 key=None, command=None):

        super().__init__(master)

        self.text = StringVar()

        self.bind("<Control-KeyPress>", AF.keypress)

        '''def func(e):
            def func_paste():
                try:
                    e.widget.delete("sel.first", "sel.last")
                except:
                    pass

                e.widget.insert(e.widget.index(INSERT), pyperclip.paste())

            def func_copy():
                try:
                    pyperclip.copy(e.widget.selection_get())
                except:
                    pass

            menu = Menu(e.widget, tearoff=0)

            menu.add_command(label=_("Paste"), command=func_paste)
            menu.add_command(label=_("Copy"), command=func_copy)

            menu.post(e.x_root, e.y_root)

        self.bind("<ButtonRelease-3>", func)'''

        self.config(textvariable=self.text)

        self.insert(0, item)

        self.bind(key, command)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for Label
class CreateLabel(Label):
    def __init__(self, master=None, text='', bg=None, anchor=None, row=0, column=0, columnspan=1, sticky='ew',
                 font=None):
        super().__init__(master)

        self.config(text=text, bg=bg, font=font)

        if anchor is not None:
            self.config(anchor=anchor)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for Checkbutton
class CreateCheckbutton(Checkbutton):
    def __init__(self, master=None, item=0, row=0, column=0):
        super().__init__(master)

        self.sel = IntVar()

        self.config(onvalue=1, offvalue=0, variable=self.sel)

        if item == 1:
            self.select()

        self.grid(row=row, column=column)


# Class for Combobox
class CreateCombobox(ttk.Combobox):
    def __init__(self, master=None, list_box=None, item='', row=0, column=0, sticky='ew',
                 state='readonly', columnspan=1, command=None):
        super().__init__(master)

        self.config(state=state)
        self['values'] = list_box

        if item != '':
            new_len = len(item)
            self.configure(width=new_len + 2)

            self.current(list_box.index(item))

        self.bind("<Control-KeyPress>", AF.keypress)
        self.bind("<Button-1>", command)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for Text
class CreateText(Text):
    def __init__(self, master=None, height=10, item='', row=0, column=0, columnspan=1, sticky='ew'):
        super().__init__(master)

        self.config(height=height)

        self.bind("<Control-KeyPress>", AF.keypress)

        self.insert(1.0, item)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for ttk.Treeview
class CreateTreeview(ttk.Treeview):
    def __init__(self, master=None, height=None, headings=None, rows=None,
                 row=None, column=None, sticky='ew', columnspan=1, selectmode="browse"):
        super().__init__(master)

        self.config(show='headings', selectmode=selectmode, height=height)

        if headings is not None:
            self["columns"] = headings
            self["displaycolumns"] = headings

            for head in headings:
                self.heading(head, text=head, anchor='w')

                if head == 'ID':
                    self.column(head, anchor='w', width=int(width_window / 64))
                else:
                    self.column(head, anchor='w')

            for col in headings:
                self.heading(col, text=col,
                             command=lambda _col=col: AF.treeview_sort_column(self, _col, False))

        if rows is not None:
            for r in rows:
                self.insert('', END, values=tuple(r))

        if row is not None:
            self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


# Class for Autocomplete Combobox
class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, row=0, column=0, columnspan=1,
                 sticky='ew', list_box='', item='', command=None,
                 events=None):
        super().__init__(master)

        self.set_completion_list(list_box)

        if item != '':
            new_len = len(item)

            self.configure(width=new_len + 2)

            self.current(list_box.index(item))

        self.bind("<Control-KeyPress>", AF.keypress)

        self.bind(events, command)

        self.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

        self.focus_set()

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        # self._completion_list = sorted(completion_list, key=str)  # Work with a sorted list
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())

        # collect hits
        _hits = []

        for element in self._completion_list:
            if element.startswith(self.get()):  # Match case insensitively
                _hits.append(element)

        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits

        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)

        # now finally perform the auto completion
        if self._hits:
            self.delete(0, END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(INSERT), END)
            self.position = self.index(END)

        if event.keysym == "Left":
            if self.position < self.index(END):  # delete the selection
                self.delete(self.position, END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, END)

        if event.keysym == "Right":
            self.position = self.index(END)  # go to end (no selection)

        if len(event.keysym) == 1:
            self.autocomplete()

        # for the Cyrillic alphabet
        if 1072 < event.keysym_num < 1103:
            self.autocomplete()
