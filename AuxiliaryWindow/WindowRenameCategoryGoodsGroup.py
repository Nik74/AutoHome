# A window where you can rename the product category group

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite

_ = AGO.t.gettext


class WindowRenameCategoryGoodsGroup(Toplevel):
    def __init__(self, element=None, parent=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Rename a goods category group"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        def rename_group():
            group_category = ()

            if element is not None:
                SQLite.upd_Category_goods_by_element(rename.get(), element)
            else:
                messagebox.showwarning(_("Error"),
                                       _('The item will not be transferred! Contact the program developer.'),
                                       parent=self)

        def rename_group_entry(event):
            rename_group()

        entry_rename = AGO.CreateEntry(master=self, row=0, column=0,
                                       key='<Return>', command=rename_group_entry)

        entry_rename.config(width=49)

        rename = entry_rename.text

        # button search
        AGO.CreateButton(master=self, text=_('Rename'), row=0, column=1,
                         command=rename_group)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)
