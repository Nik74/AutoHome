# window for create payment categories

from tkinter import *
from tkinter import messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite

_ = AGO.t.gettext


class WindowCreatePaymentCategories(Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.master = parent

        self.grab_set()

        self.title(_("Create payment categories"))

        self.iconbitmap(AGO.path_logo_ico)

        # minsize: 5
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 384)})
        self.columnconfigure(5, {'minsize': int(AGO.width_window / 384)})

        # label category name
        AGO.CreateLabel(master=self, text=_('Category name'),
                        row=0, column=1, sticky='w')

        # entry category name
        category_name = AGO.CreateEntry(master=self, row=1, column=1, columnspan=4)

        category_name.config(width=55)

        # minsize: 10
        self.rowconfigure(2, {'minsize': int(AGO.height_window / 108)})

        def save_payment_categories():
            if category_name.text.get():
                if (category_name.text.get(),) not in SQLite.sel_category_name_from_payment_categories():
                    SQLite.ins_Payment_categories(category_name.text.get())
                else:
                    messagebox.showwarning(_("Warning"),
                                           _('This payment category already exists'),
                                           parent=self)
            else:
                messagebox.showwarning(_("Warning"),
                                       _('The "Category name" field is not completed'),
                                       parent=self)

        # button
        AGO.CreateButton(master=self, text=_('Save'), row=3,
                         column=4, command=save_payment_categories)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)
