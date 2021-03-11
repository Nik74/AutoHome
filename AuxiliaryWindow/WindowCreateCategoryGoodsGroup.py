# This window is necessary to add a goods category group

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite

_ = AGO.t.gettext


class WindowCreateCategoryGoodsGroup(Toplevel):
    def __init__(self, parent='', parent_window=None):
        super().__init__(parent_window)

        self.grab_set()

        self.title(_("Create category goods group"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        # print(self.tk.eval('wm stackorder ' + str(self)+' isabove '+str(master)))

        def add_group():
            group_category = ()

            if parent == '':
                group_category = (search.get(), parent, 0)
            else:
                number = SQLite.sel_max_number_category_goods(parent)[0][0]

                if number is None:
                    number = 0
                else:
                    number += 1

                group_category = (search.get(), parent, number)

            check_category = SQLite.sel_element_category_goods()

            if (search.get(),) in check_category:
                messagebox.showwarning(_("Warning"),
                                       _('This product group already exists'),
                                       parent=self)
            else:
                SQLite.ins_Category_goods(group_category)

        def add_group_entry(event):
            add_group()

        entry_add = AGO.CreateEntry(master=self, row=0, column=0,
                                    key='<Return>', command=add_group_entry)

        # width=37
        entry_add.config(width=37)

        search = entry_add.text

        def clean_add_field():
            entry_add.delete(0, END)

        # button search
        AGO.CreateButton(master=self, text=_('Add'), row=0, column=1,
                         command=add_group)

        # button clear
        AGO.CreateButton(master=self, text=_('Clear'), row=0, column=2,
                         command=clean_add_field)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)
