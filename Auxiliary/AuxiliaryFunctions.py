import os
from tkinter import ttk
from tkinter import *

import pyperclip
import SQLite
import gettext

# object for translate message
t = gettext.translation('messages', './locale', languages=['ru'])
t.install()

_ = t.gettext


# to sort the table by column when clicking in column
def treeview_sort_column(treeview: ttk.Treeview, column, reverse: bool):
    try:
        data_list = [
            (int(treeview.set(k, column)), k) for k in treeview.get_children("")
        ]
    except Exception:
        data_list = [(treeview.set(k, column), k) for k in treeview.get_children("")]

    data_list.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(data_list):
        treeview.move(k, "", index)

    # reverse sort next time
    treeview.heading(
        column=column,
        text=column,
        command=lambda _col=column: treeview_sort_column(treeview, _col, not reverse),
    )


# function for updating information about Category_goods table
def aux_func():
    category = SQLite.sel_element_category_goods_by_parent()

    category.reverse()

    result = []

    for j in category:
        result.append(j[0])

    return result


# function for save image
def write_file(data, filename):
    try:
        with open(filename, 'wb') as file:
            file.write(data)
    except TypeError:
        with open(filename, 'w') as file:
            file.write(data)


# copy and paste on RUS keyboard layout
def keypress(e):
    if e.keycode == 86 and e.keysym != 'v':
        try:
            e.widget.delete("sel.first", "sel.last")
        except:
            pass

        e.widget.insert(e.widget.index(INSERT), pyperclip.paste())
    elif e.keycode == 67 and e.keysym != 'c':
        try:
            pyperclip.copy(e.widget.selection_get())
        except:
            pass


# function for the right mouse button
def button_3(e):
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


def printing_io(filename):
    os.startfile(filename, "print")