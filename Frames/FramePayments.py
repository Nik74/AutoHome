# This frame contains reports on payments
import os
import time

import SQLite

from tkinter import ttk, messagebox
from tkinter import *
from number_to_string import get_string_by_number
from datetime import datetime, timedelta, date
from subprocess import Popen
from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreatePayments, WindowCreateTransferFunds


_ = AGO.t.gettext

filter_date = (_('Today'), _('Yesterday'), _('Tomorrow'), _('Current month'),
               _('Last month'), _('Current week'), _('Last week'), _('Current year'),
               _('Last year'), _('All time'))

filename_PKO = 'PKO.pdf'


# main frame
class FramePayments(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.config(highlightthickness=0, bd=0)

        table = CanvasTablePayments(master=self)

        date = CanvasFilterTable(master=self, table=table.table_payments)

        CanvasButtonTop(master=self, table=table.table_payments, date=date)

        # minsize: 10
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})
        self.rowconfigure(3, {'minsize': int(AGO.height_window / 108)})

        # minsize: 10
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 192)})

        self.grid_columnconfigure(1, weight=1)

        self.master = master


# update table
def update_table(table, date_from, date_to):
    row_del = table.get_children()

    for row in row_del:
        table.delete(row)

    rows_ins = SQLite.sel_from_payments_by_payment_date(date_from, date_to)

    for row in rows_ins:
        # if payment_amount < 0, then row color - red
        if float(row[5]) < 0:
            table.insert('', END, values=row, tags=('red',))
        else:
            table.insert('', END, values=row)


# find last day this current month
def find_current_month_last_day(today: datetime) -> datetime:
    if today.month == 2:
        return today.replace(day=28)

    if today.month in [4, 6, 9, 11]:
        return today.replace(day=30)

    return today.replace(day=31)


# return first and last days this current month
def current_month_first_and_last_days() -> tuple:
    today = datetime.now()

    first_date = today.replace(day=1)

    last_date = find_current_month_last_day(today)

    return first_date, last_date


# return start and end of the week
def weekbegend(year, week):
    d = date(year, 1, 1)

    delta_days = d.isoweekday() - 1

    delta_weeks = week

    if year == d.isocalendar()[0]:
        delta_weeks -= 1

    # delta for the beginning of the week
    delta = timedelta(days=-delta_days, weeks=delta_weeks)

    weekbeg = d + delta

    # delta2 for the end of the week

    delta2 = timedelta(days=6 - delta_days, weeks=delta_weeks)

    weekend = d + delta2

    return weekbeg, weekend


def printPKO(table):
    item_payment = table.item(table.selection())

    item_PKO = SQLite.sel_for_PKO_from_payments_by_id(str(item_payment['values'][0]))

    item_PKO = list(item_PKO[0])

    payment_date = datetime.strptime(item_PKO[0], '%Y-%m-%d')
    payment_date = datetime.strftime(payment_date, '%d.%m.%Y')

    payment_id = str(item_PKO[1])

    if float(item_PKO[2]) < 0:
        payment_amount = float(item_PKO[2]) * (-1)
    else:
        payment_amount = float(item_PKO[2])

    payment_amount = round(payment_amount, 1)

    client = str(item_PKO[3])

    payment_category = str(item_PKO[4])

    currency_main = ('руб.', 'руб.', 'руб.')
    currency_additional = ('коп.', 'коп.', 'коп.')

    item_PKO.append(get_string_by_number(payment_amount, currency_main, currency_additional))

    payment_amount_words = str(item_PKO[5])

    Popen('./java/jdk-13.0.2/bin/java.exe -jar ./java/CreateCashReceiptOrder/CreateCashReceiptOrder.jar "' +
          payment_date + '" "' + payment_id + '" "' + str(payment_amount) + '" "' + client + '" "' +
          payment_category + '" "' + payment_amount_words + '"')

    time.sleep(4)

    AF.printing_io(filename_PKO)

    time.sleep(8)

    os.system('taskkill /im AcroRd32.exe /f')

    time.sleep(3)

    os.remove(filename_PKO)


# button top
class CanvasButtonTop(Canvas):
    def __init__(self, master=None, table=None, date=None):
        super().__init__(master)

        self.master = master

        self.config(highlightthickness=0, bd=0)

        def create_payments():
            WindowCreatePayments.WindowCreatePayments(parent=master.master)

        def upd_payments_table():
            update_table(table, date.from_date.get(), date.to_date.get())

            date.payments_amount_sum.config(state=NORMAL)

            date.payments_amount_sum.delete(0, END)

            date.payments_amount_sum.insert(END, SQLite.sel_sum_payment_amount_from_payments())

            date.payments_amount_sum.config(state=DISABLED)

        def create_transfer():
            WindowCreateTransferFunds.WindowCreateTransferFunds(parent=master.master)

        def print_PKO():
            printPKO(table)

        # button update
        AGO.CreateButton(master=self, text=_('Update'), row=0, column=0,
                         command=upd_payments_table)

        # button print PKO
        AGO.CreateButton(master=self, text=_('Print PKO'), row=0,
                         column=1, command=print_PKO)

        # button create payment
        AGO.CreateButton(master=self, text=_('Create payment'), row=0,
                         column=2, command=create_payments)

        # button transfer of funds
        AGO.CreateButton(master=self, text=_('Transfer funds'), row=0,
                         column=3, command=create_transfer)

        self.grid(row=0, column=0, sticky='w')


# filtering the table by date and displaying the total amount of payments
class CanvasFilterTable(Canvas):
    def __init__(self, master=None, table=None):
        super().__init__(master)

        self.master = master

        self.config(highlightthickness=0, bd=0)

        # label payment date
        AGO.CreateLabel(master=self, text=_('Payment date:'), row=0,
                        column=0)

        # auxiliary function for date filter
        def aux_func(date_1=None, date_2=None):
            if date_2 is None:
                self.from_date.set_date(date_1.strftime('%d.%m.%Y'))

                self.to_date.set_date(date_1.strftime('%d.%m.%Y'))

                update_table(table, date_1, date_1)
            else:
                self.from_date.set_date(date_1.strftime('%d.%m.%Y'))

                self.to_date.set_date(date_2.strftime('%d.%m.%Y'))

                update_table(table, date_1, date_2)

        def change_date(e):
            if e.widget.get() == _('Today'):
                date_now = datetime.now()

                aux_func(date_1=date_now)
            elif e.widget.get() == _('Yesterday'):
                yesterday = datetime.now() - timedelta(1)

                aux_func(date_1=yesterday)
            elif e.widget.get() == _('Tomorrow'):
                tomorrow = datetime.now() + timedelta(1)

                aux_func(date_1=tomorrow)
            elif e.widget.get() == _('Current month'):
                aux_func(date_1=begin_month, date_2=end_month)
            elif e.widget.get() == _('Last month'):
                end_last_month = begin_month - timedelta(1)

                begin_last_month = end_last_month.replace(day=1)

                aux_func(date_1=begin_last_month, date_2=end_last_month)
            elif e.widget.get() == _('Current week'):
                today = datetime.today()

                num_current_week = today.strftime("%U")

                begin_current_week, end_current_week = weekbegend(datetime.now().year,
                                                                  int(num_current_week))

                aux_func(date_1=begin_current_week, date_2=end_current_week)
            elif e.widget.get() == _('Last week'):
                today = datetime.today()

                num_current_week = today.strftime("%U")

                begin_current_week, end_current_week = weekbegend(datetime.now().year,
                                                                  int(num_current_week) - 1)

                aux_func(date_1=begin_current_week, date_2=end_current_week)
            elif e.widget.get() == _('Current year'):
                current_date = datetime.now()

                first_day_current_year = datetime(current_date.year, 1, 1).date()

                last_day_current_year = datetime(current_date.year, 12, 31).date()

                aux_func(date_1=first_day_current_year, date_2=last_day_current_year)
            elif e.widget.get() == _('Last year'):
                current_date = datetime.now()

                first_day_current_year = datetime(current_date.year - 1, 1, 1).date()

                last_day_current_year = datetime(current_date.year - 1, 12, 31).date()

                aux_func(date_1=first_day_current_year, date_2=last_day_current_year)
            elif e.widget.get() == _('All time'):
                try:
                    start_date = datetime.strptime(SQLite.sel_min_payment_date_from_Payments()[0][0],
                                                   '%Y-%m-%d').date()
                    end_date = datetime.strptime(SQLite.sel_max_payment_date_from_Payments()[0][0],
                                                 '%Y-%m-%d').date()

                    aux_func(date_1=start_date, date_2=end_date)
                except TypeError:
                    messagebox.showwarning(_("Warning"),
                                           _('The Payment table in the database is empty'),
                                           parent=self)

        # combobox payment date
        filter_payment_date = AGO.CreateCombobox(master=self, list_box=filter_date, item=filter_date[3],
                                                 row=0, column=1, command=change_date)

        filter_payment_date.config(width=17)

        # label from
        AGO.CreateLabel(master=self, text=_('from'), row=0,
                        column=2)

        begin_month, end_month = current_month_first_and_last_days()

        def sel_date(e):
            update_table(table, self.from_date.get(), self.to_date.get())

        # DateEntry from
        self.from_date = AGO.CreateDateEntry(master=self, row=0, column=3,
                                             events="<<DateEntrySelected>>",
                                             command=sel_date)

        self.from_date.set_date(begin_month.strftime('%d.%m.%Y'))

        # label to
        AGO.CreateLabel(master=self, text=_('to'), row=0,
                        column=4)

        # DateEntry to
        self.to_date = AGO.CreateDateEntry(master=self, row=0, column=5,
                                           events="<<DateEntrySelected>>",
                                           command=sel_date)

        self.to_date.set_date(end_month.strftime('%d.%m.%Y'))

        # for get date use <<DateEntrySelected>>

        # label total payments for all time
        AGO.CreateLabel(master=self, text=_('Total payments for all time'),
                        row=0, column=6)

        total_payments = SQLite.sel_sum_payment_amount_from_payments()

        # entry total payments for all time
        self.payments_amount_sum = AGO.CreateEntry(master=self, row=0, column=7,
                                                   item=total_payments)

        self.payments_amount_sum.config(state=DISABLED, font='bold')

        self.grid(row=2, column=0, sticky='ew')


# table payments
class CanvasTablePayments(Canvas):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        # height = 890
        self.config(height=int(AGO.height_window / 1.213483146067416),
                    highlightthickness=0, bd=0)

        headings = ('ID', _('Payment date'), _('Payment type'),
                    _('Payment storage location'), _('Payment category'),
                    _('Payment amount'), _('Move_from'),
                    _('Move_to'), _('Client'), _('Order'),
                    _('Created'), _('Created by'), _('Employee'), _('Company'))

        date_from, date_to = current_month_first_and_last_days()

        rows = SQLite.sel_from_payments_by_payment_date(date_from, date_to)

        # height=43
        self.table_payments = AGO.CreateTreeview(master=self, height=int(AGO.height_window / 25.11627906976744),
                                                 headings=headings, row=0, column=0)

        self.table_payments.tag_configure('red', background='#fc9dad')

        # to highlight a row
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

        for row in rows:
            # if payment_amount < 0, then row color - red
            if float(row[5]) < 0:
                self.table_payments.insert('', END, values=row, tags=('red',))
            else:
                self.table_payments.insert('', END, values=row)

        def right_click_menu(e):
            def delete_row():
                id_payments = str(self.table_payments.set(row_id)['ID'])

                payment_amount, payment_category = SQLite.sel_amount_category_from_payments_by_id(id_payments)[0]

                # if the payment category is 'перемещение средств',
                # then we delete both payments for the transfer of funds
                if payment_category == 'Перемещение средств':
                    if int(payment_amount) < 0:
                        payment_amount2, payment_category2 = \
                            SQLite.sel_amount_category_from_payments_by_id(int(id_payments) + 1)[0]

                        if payment_category == payment_category2 and \
                                int(payment_amount) == int(payment_amount2) * (-1):
                            SQLite.del_row_Payments_by_id(id_payments)
                            SQLite.del_row_Payments_by_id(int(id_payments) + 1)

                    elif int(payment_amount) > 0:
                        payment_amount2, payment_category2 = \
                            SQLite.sel_amount_category_from_payments_by_id(int(id_payments) - 1)[0]

                        if payment_category == payment_category2 and \
                                int(payment_amount) == int(payment_amount2) * (-1):
                            SQLite.del_row_Payments_by_id(id_payments)
                            SQLite.del_row_Payments_by_id(int(id_payments) - 1)
                else:
                    SQLite.del_row_Payments_by_id(id_payments)

                update_table(self.table_payments, date_from, date_to)

            def print_PKO():
                printPKO(self.table_payments)

            # create a popup menu
            row_id = self.table_payments.identify('item', e.x, e.y)

            if row_id:
                self.table_payments.selection_set(row_id)
                self.table_payments.focus_set()
                self.table_payments.focus(row_id)

                menu = Menu(self, tearoff=0)

                menu.add_command(label=_('Print PKO'), command=print_PKO)
                menu.add_command(label=_("Delete"), command=delete_row)

                menu.post(e.x_root, e.y_root)
            else:
                pass

        def select_payment(e):
            item_payment = self.table_payments.item(self.table_payments.selection())

            row_id_payment = self.table_payments.identify('item', e.x, e.y)

            if row_id_payment:
                try:
                    if str(item_payment['values'][6]) == 'None':
                        WindowCreatePayments.WindowCreatePayments(parent=master.master,
                                                                  id_payments=str(item_payment['values'][0]))
                    else:
                        pass
                except IndexError:
                    pass
            else:
                pass

        self.table_payments.bind("<Button-3>", right_click_menu)
        self.table_payments.bind("<Double-1>", select_payment)

        def rec_canvas(event):
            self.configure(scrollregion=self.bbox('all'))

        scrollbar_table_payments = Scrollbar(master, orient=HORIZONTAL)

        scrollbar_table_payments["command"] = self.xview
        self["xscrollcommand"] = scrollbar_table_payments.set

        self.create_window((0, 0), window=self.table_payments, anchor="nw")

        self.table_payments.bind("<Configure>", rec_canvas)

        scrollbar_table_payments.grid(row=5, column=0, sticky='ew', columnspan=2)

        self.grid(row=4, column=0, sticky='ew', columnspan=2)
