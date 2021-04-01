# in this window, the transfer of funds is performed
from datetime import datetime

import SQLite

from tkinter import ttk, messagebox
from tkinter import *
from Auxiliary import AuxiliaryGlobalObject as AGO

_ = AGO.t.gettext

transfer_funds_category = 'Перемещение средств'

payment_type = (_('Cash'), _('Non-cash'))


class WindowCreateTransferFunds(Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Create transfer funds"))

        self.iconbitmap(AGO.path_logo_ico)

        self.config(highlightthickness=0, bd=0)

        style = ttk.Style()
        style.theme_use('vista')

        CanvasTransferFunds(master=self)

        # minsize: 5
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 384)})
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 384)})
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)


class CanvasTransferFunds(Canvas):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        self.config(highlightthickness=0, bd=0)

        inf_transfer = dict()

        inf_transfer['Payment_category'] = transfer_funds_category

        if (transfer_funds_category,) not in SQLite.sel_category_name_from_payment_categories():
            SQLite.ins_Payment_categories(transfer_funds_category)

        # label amount of funds transferred
        AGO.CreateLabel(master=self, text=_('Amount of funds transferred (positive amount)'),
                        row=0, column=0, sticky='w')

        # entry amount of funds transferred
        inf_transfer['Transfer_payment_amount'] = AGO.CreateEntry(master=self,
                                                                  row=1, column=0,
                                                                  columnspan=3).text
        # label move_from
        AGO.CreateLabel(master=self, text=_('From where to move (original storage location)'),
                        row=2, column=0, sticky='w')

        payment_storage_locations = []

        for p_s_l in SQLite.sel_payment_storage_locations_from_payment_storage_locations():
            if p_s_l != ('',):
                payment_storage_locations.append('.'.join(p_s_l))

        # combobox old payment storage location
        inf_transfer['Old_payment_storage_location'] = AGO.CreateCombobox(master=self,
                                                                          list_box=payment_storage_locations,
                                                                          row=3, column=0, columnspan=3)
        # label move_to
        AGO.CreateLabel(master=self, text=_('Where to move (final storage location)'),
                        row=4, column=0, sticky='w')

        # combobox new payment storage location
        inf_transfer['New_payment_storage_location'] = AGO.CreateCombobox(master=self,
                                                                          list_box=payment_storage_locations,
                                                                          row=5, column=0, columnspan=3)
        # label note
        AGO.CreateLabel(master=self, text=_('Note'), row=6, column=0, sticky='w')

        # entry note
        inf_transfer['Note'] = AGO.CreateEntry(master=self, row=7, column=0,
                                               columnspan=3).text
        # label payment type
        AGO.CreateLabel(master=self, text=_('Payment type'), row=8, column=0,
                        sticky='w')

        # combobox payment type
        inf_transfer['Payment_type'] = AGO.CreateCombobox(master=self, list_box=payment_type,
                                                          row=9, column=0, columnspan=3)

        # label company
        AGO.CreateLabel(master=self, text=_('Company'), row=10, column=0,
                        sticky='w')

        # entry company
        inf_transfer['Company'] = AGO.CreateEntry(master=self, row=11, column=0,
                                                  columnspan=3).text

        # label payment date
        AGO.CreateLabel(master=self, text=_('Payment date'), row=12, column=0,
                        sticky='w')

        inf_transfer['Payment_date'] = AGO.CreateDateEntry(master=self, row=13,
                                                           column=0, columnspan=3,
                                                           date_pattern='yyyy-mm-dd')
        date_now = datetime.now()

        inf_transfer['Date_create'] = date_now.strftime('%Y-%m-%d')

        # Save and exit
        def save_payment_and_exit():
            inf_tr = list()

            if inf_transfer.get('Transfer_payment_amount').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Amount of funds transferred" field is not completed'),
                                       parent=self)
                return 0

            if ',' in inf_transfer.get('Transfer_payment_amount').get():
                messagebox.showwarning(_("Warning"),
                                       _('In the "Amount of funds transferred" field, the fractional number '
                                         'must be separated by a dot'), parent=self)
                return 0

            if inf_transfer.get('Old_payment_storage_location').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Where to move from" field is not completed'),
                                       parent=self)
                return 0

            if inf_transfer.get('New_payment_storage_location').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Where to move" field is not completed'),
                                       parent=self)
                return 0

            if inf_transfer.get('Old_payment_storage_location').get() == \
                    inf_transfer.get('New_payment_storage_location').get():
                messagebox.showwarning(_("Warning"),
                                       _('The old storage location must be different from the new storage location'),
                                       parent=self)
                return 0

            if inf_transfer.get('Payment_type').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment type" field is not completed'),
                                       parent=self)
                return 0

            if inf_transfer.get('Payment_date').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment date" field is not completed'),
                                       parent=self)
                return 0

            for i in inf_transfer.values():
                if type(i) is str:
                    inf_tr.append(i)
                else:
                    inf_tr.append(i.get())

            try:
                inf_tr[1] = int(inf_tr[1])
            except ValueError:
                messagebox.showwarning(_("Warning"),
                                       _('In the "Amount of funds transferred" field, enter a number'),
                                       parent=self)

                return 0

            inf_tr.append(inf_transfer.get('Old_payment_storage_location').get())

            inf_tr[1] = inf_tr[1] * (-1)

            SQLite.ins_Payments_for_transfer(inf_tr)

            inf_tr[1] = inf_tr[1] * (-1)

            inf_tr[9] = inf_transfer['New_payment_storage_location'].get()

            SQLite.ins_Payments_for_transfer(inf_tr)

            master.destroy()

        # minsize: 5
        self.rowconfigure(14, {'minsize': int(AGO.height_window / 216)})

        # button save
        AGO.CreateButton(master=self, text=_('Save and exit'), command=save_payment_and_exit,
                         row=15, column=2)

        self.grid(row=0, column=1, sticky='ew')
