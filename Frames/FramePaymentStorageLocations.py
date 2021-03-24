# In this frame, payment storage locations are created and displayed

from tkinter import *
from Auxiliary import AuxiliaryGlobalObject as AGO
from AuxiliaryWindow import WindowCreatePaymentStorageLocations

import SQLite

_ = AGO.t.gettext


# main frame
class FramePaymentStorageLocations(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        table = CanvasTablePaymentStorageLocations(master=self)

        CanvasButtonTop(master=self, table=table.table_payment_storage_locations)

        # minsize: 10
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

        self.master = master


# update table
def update_table(table):
    row_del = table.get_children()

    for row in row_del:
        table.delete(row)

    rows_ins = SQLite.sel_from_payment_storage_locations()

    for row in rows_ins:
        table.insert('', END, values=row)


# canvas button
class CanvasButtonTop(Canvas):
    def __init__(self, master=None, table=None):
        super().__init__(master)

        self.master = master

        def upd_table():
            update_table(table)

        def create_payment_categories():
            WindowCreatePaymentStorageLocations.WindowCreatePaymentStorageLocations(parent=self.master.master)

        AGO.CreateButton(master=self, text=_("Update"),
                         row=0, column=0, command=upd_table)

        AGO.CreateButton(master=self, text=_("Create payment storage locations"),
                         row=0, column=1, command=create_payment_categories)

        self.grid(row=0, column=0, sticky='w')


# canvas table payment storage locations
class CanvasTablePaymentStorageLocations(Canvas):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        headings = ('ID', _('Payment storage location'))

        rows = SQLite.sel_from_payment_storage_locations()

        # height = 46
        self.table_payment_storage_locations = AGO.CreateTreeview(master=self,
                                                                  height=int(AGO.height_window / 23.47826086956522),
                                                                  headings=headings, rows=rows, row=0,
                                                                  column=0)

        self.table_payment_storage_locations.column(_('Payment storage location'), width=500)

        def right_click_menu(e):
            def delete_row():
                id_payment_storage_locations = str(self.table_payment_storage_locations.set(row_id)['ID'])

                SQLite.del_row_Payment_storage_locations_by_id(id_payment_storage_locations)

                update_table(self.table_payment_storage_locations)

            # create a popup menu
            row_id = self.table_payment_storage_locations.identify('item', e.x, e.y)

            if row_id:
                self.table_payment_storage_locations.selection_set(row_id)
                self.table_payment_storage_locations.focus_set()
                self.table_payment_storage_locations.focus(row_id)

                menu = Menu(self, tearoff=0)
                menu.add_command(label=_("Delete"), command=delete_row)
                menu.post(e.x_root, e.y_root)
            else:
                pass

        self.table_payment_storage_locations.bind("<Button-3>", right_click_menu)

        self.grid(row=2, column=0)
