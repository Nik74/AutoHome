from tkinter import *
from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreateClient as WCC, WindowCreateCar as WCCar

import SQLite

_ = AGO.t.gettext


class FrameClients(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.buttons_top()
        self.search_field()

        if AGO.width_window < 1360:
            # minsize: 15
            self.columnconfigure(5, {'minsize': int(AGO.width_window / 128)})
            self.grid_columnconfigure(5, weight=1)

        self.table = CanvasClientTree(self).table_client

    # command for button of update
    def update_table(self):
        row_del = self.table.get_children()

        for row in row_del:
            self.table.delete(row)

        rows_ins = SQLite.sel_from_clients()

        for row in rows_ins:
            self.table.insert('', END, values=tuple(row))

    # Buttons on top
    def buttons_top(self):
        # command for create client
        def create_client():
            WCC.WindowCreateClient(parent=self.master)

        # command for create car
        def create_car():
            WCCar.WindowCreateCar(parent=self.master)

        # button update
        AGO.CreateButton(master=self, text=_('Update'), command=self.update_table,
                         row=0, column=0)

        # button create client
        AGO.CreateButton(master=self, text=_('Create client'), command=create_client,
                         bg='yellow', row=0, column=1)

        # button create car client
        AGO.CreateButton(master=self, text=_('Create an car client'),
                         row=0, column=2, command=create_car)

        # minsize: 15
        for i in range(1, 4):
            self.rowconfigure(i, {'minsize': int(AGO.height_window / 72)})

    # Search field
    def search_field(self):
        def search_command():
            row_del = self.table.get_children()

            for row in row_del:
                self.table.delete(row)

            rows_ins = SQLite.sel_from_clients_by_client(search.get())

            for row in rows_ins:
                self.table.insert('', END, values=tuple(row))

        def search_entry(event):
            search_command()

        # entry search
        entry_search = AGO.CreateEntry(master=self, row=5, column=0, columnspan=3,
                                       key='<Return>', command=search_entry)

        search = entry_search.text

        def clean_search_field():
            entry_search.delete(0, END)
            self.update_table()

        # button search
        AGO.CreateButton(master=self, text=_('Search'), row=5, column=3,
                         command=search_command)

        # button clear
        AGO.CreateButton(master=self, text=_('Clear'), row=5, column=4,
                         command=clean_search_field)

        # minsize: 30
        for i in range(6, 7):
            self.rowconfigure(i, {'minsize': int(AGO.height_program / 36)})


# command for button of update
def update_table(table):
    row_del = table.get_children()

    for row in row_del:
        table.delete(row)

    rows_ins = SQLite.sel_from_clients()

    for row in rows_ins:
        table.insert('', END, values=tuple(row))


# Canvas for client table
class CanvasClientTree(Canvas):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.config(highlightthickness=0, bd=0)

        self.del_car = ''

        headings = ('ID', _('Client'), _('Phone number'), _('Number car'),
                    _('Type client'), _('Mark car'))

        rows = SQLite.sel_from_clients()

        def rec_canvas(event):
            self.configure(scrollregion=self.bbox('all'))

        self.table_client = AGO.CreateTreeview(master=self, headings=headings, height=12,
                                               rows=rows, row=0, column=0)

        self.table_car = AGO.CreateTreeview(master=self, height=4)

        def show_car_table(event):
            if type(self.del_car) is CanvasTableCar:
                self.del_car.destroy()
                self.del_car.scrollbar_table_car.destroy()

            # minsize: 10
            self.rowconfigure(9, {'minsize': int(AGO.height_window / 108)})

            row_id = self.table_client.identify_row(event.y)

            if row_id:
                self.del_car = CanvasTableCar(master, row_id, self.table_client)
            else:
                try:
                    self.table_client.selection_remove(self.table_client.selection()[0])
                except IndexError:
                    pass

        def select(e):
            item = self.table_client.item(self.table_client.selection())

            row_id = self.table_client.identify('item', e.x, e.y)

            if row_id:
                try:
                    WCC.WindowCreateClient(id=str(item['values'][0]))
                except IndexError:
                    pass
            else:
                pass

        def right_click_menu(e):
            def delete_row():
                SQLite.del_row_Clients(str(self.table_client.set(row_id)['ID']))
                SQLite.del_row_Car_by_client(str(self.table_client.set(row_id)[_('Client')]))

                update_table(self.table_client)

                if type(self.del_car) is CanvasTableCar:
                    self.del_car.destroy()
                    self.del_car.scrollbar_table_car.destroy()

            # create a popup menu
            row_id = self.table_client.identify('item', e.x, e.y)

            if row_id:
                self.table_client.selection_set(row_id)
                self.table_client.focus_set()
                self.table_client.focus(row_id)

                menu = Menu(self, tearoff=0)
                menu.add_command(label=_("Delete"), command=delete_row)
                menu.post(e.x_root, e.y_root)
            else:
                pass

        self.table_client.bind("<Double-1>", select)

        self.table_client.bind("<Button-3>", right_click_menu)

        self.table_client.bind("<1>", show_car_table)

        for col in headings:
            self.table_client.heading(col, text=col,
                                      command=lambda _col=col: AF.treeview_sort_column(self.table_client,
                                                                                       _col, False))

        if AGO.width_window < 1360:
            scrollbar_table_client = Scrollbar(master, orient=HORIZONTAL)

            scrollbar_table_client["command"] = self.xview
            self["xscrollcommand"] = scrollbar_table_client.set

            self.create_window((0, 0), window=self.table_client, anchor="nw")

            self.table_client.bind("<Configure>", rec_canvas)
            scrollbar_table_client.grid(row=8, column=0, columnspan=100, sticky='ew')

        self.grid_columnconfigure(0, weight=1)

        self.grid(row=7, column=0, columnspan=100, sticky='ew')


# Canvas for car table
class CanvasTableCar(Canvas):
    def __init__(self, master=None, row_id=None, table=None, root=None):
        super().__init__(master)
        self.master = master

        # height = 115
        self.config(height=int(AGO.height_window / 9.391304347826087))

        self.scrollbar_table_car = Scrollbar(master, orient=HORIZONTAL)

        def rec_canvas(event):
            self.configure(scrollregion=self.bbox('all'))

        if row_id:
            table.selection_set(row_id)

            # command for update
            def update_table_car():
                row_del_car = self.table_car.get_children()

                for row_t_car in row_del_car:
                    self.table_car.delete(row_t_car)

                rows_ins_car = SQLite.sel_from_car(str(table.set(row_id)[_('Client')]))

                for row_t_car in rows_ins_car:
                    self.table_car.insert('', END, values=tuple(row_t_car))

            headings_car = ('ID', _('Mark Model'), 'VIN', _('Client'),
                            _('Year of release'), _('Name'))

            rows_car = SQLite.sel_from_car(str(table.set(row_id)[_('Client')]))

            self.table_car = AGO.CreateTreeview(master=self, height=4, headings=headings_car,
                                                rows=rows_car, row=0, column=0, columnspan=100)

            self.table_car.column(_('Name'), anchor='w', width=400)

            def select_car(event):
                item_car = self.table_car.item(self.table_car.selection())

                row_id_car = self.table_car.identify('item', event.x, event.y)

                if row_id_car:
                    try:
                        WCCar.WindowCreateCar(id=str(item_car['values'][0]))
                    except IndexError:
                        pass
                else:
                    pass

            def right_click_menu_car(event):
                def delete_row_car():
                    SQLite.del_row_Car_by_id(str(self.table_car.set(row_id_car)['ID']))

                    update_table_car()

                # create a popup menu
                row_id_car = self.table_car.identify('item', event.x, event.y)

                if row_id_car:
                    self.table_car.selection_set(row_id_car)
                    self.table_car.focus_set()
                    self.table_car.focus(row_id_car)

                    menu = Menu(self, tearoff=0)
                    menu.add_command(label=_("Delete"), command=delete_row_car)
                    menu.post(event.x_root, event.y_root)
                else:
                    pass

            self.table_car.bind("<Double-1>", select_car)

            self.table_car.bind("<Button-3>", right_click_menu_car)

            if AGO.width_window < 1440:
                self.scrollbar_table_car["command"] = self.xview
                self["xscrollcommand"] = self.scrollbar_table_car.set

                self.create_window((0, 0), window=self.table_car, anchor="nw")

                self.table_car.bind("<Configure>", rec_canvas)
                self.scrollbar_table_car.grid(row=11, column=0, columnspan=100, sticky='ew')

            self.grid(row=10, column=0, columnspan=100, sticky='ew')
