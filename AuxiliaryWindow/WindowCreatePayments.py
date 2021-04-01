# this is where the payment is created
from datetime import datetime

import SQLite

from tkinter import *
from tkinter import messagebox, ttk
from Auxiliary import AuxiliaryGlobalObject as AGO

_ = AGO.t.gettext

payment_type = (_('Cash'), _('Non-cash'))


class WindowCreatePayments(Toplevel):
    def __init__(self, parent=None, id_payments=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Create payments"))

        self.iconbitmap(AGO.path_logo_ico)

        self.config(highlightthickness=0, bd=0)

        style = ttk.Style()
        style.theme_use('vista')

        # minsize: 5
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 384)})
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 384)})
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        CanvasInfPayment(master=self, id_payments=id_payments)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)


class CanvasInfPayment(Canvas):
    def __init__(self, master=None, id_payments=None):
        super().__init__(master)

        self.master = master

        self.config(highlightthickness=0, bd=0)

        item = ['' for x in range(0, 8)]

        if id_payments is not None:
            sel_payments = SQLite.sel_from_payments_by_id(id_payments)

            if sel_payments is not None:
                item = sel_payments[0]

        inf_payments = dict()

        # label payment amount
        AGO.CreateLabel(master=self, text=_('Payment amount'),
                        row=0, column=0, sticky='w')

        # entry payment amount
        inf_payments['Payment_amount'] = AGO.CreateEntry(master=self,
                                                         row=1, column=0,
                                                         item=item[0],
                                                         columnspan=3).text

        # label note
        AGO.CreateLabel(master=self, text=_('Note'), row=2, column=0, sticky='w')

        # entry note
        inf_payments['Note'] = AGO.CreateEntry(master=self, row=3, column=0,
                                               item=item[1],
                                               columnspan=3).text
        # label payment category
        AGO.CreateLabel(master=self, text=_('Payment category'), row=4,
                        column=0, sticky='w')

        payment_category = []

        for p_c in SQLite.sel_category_name_from_payment_categories():
            if p_c != ('',):
                payment_category.append('.'.join(p_c))

        # combobox payment category
        inf_payments['Payment_category'] = AGO.CreateCombobox(master=self,
                                                              list_box=payment_category,
                                                              item=item[2], row=5,
                                                              column=0,
                                                              columnspan=3)
        # label payment storage location
        AGO.CreateLabel(master=self, text=_('Payment storage location'),
                        row=6, column=0, sticky='w')

        payment_storage_locations = []

        for p_s_l in SQLite.sel_payment_storage_locations_from_payment_storage_locations():
            if p_s_l != ('',):
                payment_storage_locations.append('.'.join(p_s_l))

        # combobox payment storage location
        inf_payments['Payment_storage_location'] = AGO.CreateCombobox(master=self,
                                                                      list_box=payment_storage_locations,
                                                                      item=item[3], row=7, column=0,
                                                                      columnspan=3)
        # label payment type
        AGO.CreateLabel(master=self, text=_('Payment type'), row=8, column=0,
                        sticky='w')

        # combobox payment type
        inf_payments['Payment_type'] = AGO.CreateCombobox(master=self, list_box=payment_type,
                                                          item=item[4], row=9, column=0,
                                                          columnspan=3)
        # label company
        AGO.CreateLabel(master=self, text=_('Company'), row=10, column=0,
                        sticky='w')

        # entry company
        inf_payments['Company'] = AGO.CreateEntry(master=self, row=11, column=0,
                                                  item=item[5], columnspan=3).text
        # label payment date
        AGO.CreateLabel(master=self, text=_('Payment date'), row=12, column=0,
                        sticky='w')

        item6 = ''

        # date entry payment date
        if item[6] != '':
            item6 = datetime.strptime(item[6], '%Y-%m-%d')

        inf_payments['Payment_date'] = AGO.CreateDateEntry(master=self, row=13,
                                                           column=0, item=item6,
                                                           columnspan=3,
                                                           date_pattern='yyyy-mm-dd')

        if id_payments is not None:
            inf_payments['Date_create'] = item[7]
        else:
            date_now = datetime.now()

            inf_payments['Date_create'] = date_now.strftime('%Y-%m-%d')

        # Save and exit
        def save_payment_and_exit():
            inf_pay = list()

            if inf_payments.get('Payment_amount').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment amount" field is not completed'),
                                       parent=self)
                return 0

            if ',' in inf_payments.get('Payment_amount').get():
                messagebox.showwarning(_("Warning"),
                                       _('In the "Payment amount" field, the fractional number '
                                         'must be separated by a dot'), parent=self)
                return 0

            if inf_payments.get('Payment_category').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment category" field is not completed'),
                                       parent=self)
                return 0

            if inf_payments.get('Payment_storage_location').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment storage location" field is not completed'),
                                       parent=self)
                return 0

            if inf_payments.get('Payment_type').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment type" field is not completed'),
                                       parent=self)
                return 0

            if inf_payments.get('Payment_date').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Payment date" field is not completed'),
                                       parent=self)
                return 0

            for i in inf_payments.values():
                if type(i) is str:
                    inf_pay.append(i)
                else:
                    inf_pay.append(i.get())

            if id_payments is not None:
                inf_pay.append(id_payments)

                SQLite.upd_payments_by_id(inf_pay)
            else:
                SQLite.ins_Payments(inf_pay)

            master.destroy()

        # minsize: 5
        self.rowconfigure(14, {'minsize': int(AGO.height_window / 216)})

        # button save
        AGO.CreateButton(master=self, text=_('Save and exit'), command=save_payment_and_exit,
                         row=15, column=2)

        self.grid(row=0, column=1, sticky='ew')
