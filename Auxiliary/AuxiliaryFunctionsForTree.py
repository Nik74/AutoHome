from tkinter import BOTH
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite


# Adding a list to the tree from a base data
def add_list_to_tree_from_bd(tree):
    result = ''

    for line in SQLite.sel_from_tab():
        if line[1] == 'Car service':
            result = line[1]

        tree.insert(line[2], line[3], line[1], text=line[4])

    return result


# Adding a list to the goods tree from a base data
def add_list_goods_tree_from_bd(tree):
    for line in SQLite.sel_all_category_goods_by_parent():
        tree.insert(line[2], line[3], line[1], text=line[1])

    for line in SQLite.sel_all_category_goods_by_parent_2():
        tree.insert(line[2], line[3], line[1], text=line[1])


# Outputs frame with parameters pack(padx=10, pady=10, fill=BOTH)
def pack_out(frame):
    frame.pack(padx=int(AGO.width_window / 192), pady=int(AGO.height_window / 108), fill=BOTH)
