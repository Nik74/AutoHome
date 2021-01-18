from tkinter import ttk, BOTH
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite


# Adding a list to the tree from a base data
def add_list_to_tree_from_bd(tree: ttk.Treeview):
    result = ''

    for line in SQLite.sel_from_tab():
        if line[1] == 'Car service':
            result = line[1]

        tree.insert(line[2], line[3], line[1], text=line[4])

    return result


# Outputs frame with parameters pack(padx=10, pady=10, fill=BOTH)
def pack_out(frame):
    frame.pack(padx=int(AGO.width_window / 192), pady=int(AGO.height_window / 108), fill=BOTH)


# Hide frame
def hide_frame(frame):
    frame.pack_forget()
