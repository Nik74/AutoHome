# create payment storage locations

from tkinter import *
from tkinter import messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite

_ = AGO.t.gettext


class WindowCreatePaymentStorageLocations(Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.master = parent

        self.grab_set()

        self.title(_("Create payment storage locations"))

        self.iconbitmap(AGO.path_logo_ico)

        # minsize: 5
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 384)})
        self.columnconfigure(5, {'minsize': int(AGO.width_window / 384)})

        # label payment storage location
        AGO.CreateLabel(master=self, text=_('Payment storage location'),
                        row=0, column=1, sticky='w')

        # entry category name
        payment_storage_locations = AGO.CreateEntry(master=self, row=1, column=1, columnspan=4)

        payment_storage_locations.config(width=56)

        # minsize: 10
        self.rowconfigure(2, {'minsize': int(AGO.height_window / 108)})

        def save_payment_storage_locations():
            if payment_storage_locations.text.get():
                if (payment_storage_locations.text.get(),) not in \
                        SQLite.sel_payment_storage_locations_from_payment_storage_locations():
                    SQLite.ins_Payment_storage_locations(payment_storage_locations.text.get())
                else:
                    messagebox.showwarning(_("Warning"),
                                           _('This payment storage location already exists'),
                                           parent=self)
            else:
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment storage location" field is not completed'),
                                       parent=self)

        # button
        AGO.CreateButton(master=self, text=_('Save'), row=3,
                         column=4, command=save_payment_storage_locations)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)
