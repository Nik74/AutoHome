from tkinter import *
from tkinter import ttk

from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreateClient as WCC, WindowCreateCar as WCCar
import SQLite

_ = AGO.t.gettext


# command for create client
def create_client():
    WCC.WindowCreateClient()


# command for create car
def create_car():
    WCCar.WindowCreateCar()


class FrameClients(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.buttons_top()
        self.search_field()

        self.table = ttk.Treeview(self, show="headings", selectmode="browse")

        self.out_client()

    # command for button of update
    def update_table(self):
        Label(self, height=8).grid(row=10, column=0, columnspan=100, sticky='ew')

        row_del = self.table.get_children()

        for row in row_del:
            self.table.delete(row)

        rows_ins = SQLite.sel_from_clients()

        for row in rows_ins:
            self.table.insert('', END, values=tuple(row))

    # Buttons on top
    def buttons_top(self):
        # button update
        AGO.CreateButton(master=self, text=_('Update'), command=self.update_table,
                         row=0, column=0)

        # button create client
        AGO.CreateButton(master=self, text=_('Create client'), command=create_client,
                         bg='yellow', row=0, column=1)

        # button create car client
        AGO.CreateButton(master=self, text=_('Create an car client'), bg='yellow',
                         row=0, column=2, command=create_car)

        # button open card
        AGO.CreateButton(master=self, text=_('Open a card'), bg='red', row=0,
                         column=3, columnspan=2)

        # minsize: 15
        for i in range(1, 4):
            self.rowconfigure(i, {'minsize': int(AGO.height_window / 72)})

    # Search field
    def search_field(self):
        def search_command():
            Label(self, height=8).grid(row=10, column=0, columnspan=100, sticky='ew')

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

    # The output data of the clients
    def out_client(self):
        headings = ('ID', _('Client'), _('Phone number'), _('Number car'),
                    _('Type client'), _('Mark car'))

        rows = SQLite.sel_from_clients()

        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for head in headings:
            self.table.heading(head, text=head, anchor='w')

            if head == 'ID':
                # width = 15
                self.table.column(head, anchor='w',
                                  width=int(AGO.width_window / 64))
            else:
                self.table.column(head, anchor='w')

        for row in rows:
            self.table.insert('', END, values=tuple(row))

        def select(e):
            item = self.table.item(self.table.selection())

            row_id = self.table.identify('item', e.x, e.y)

            if row_id:
                try:
                    WCC.WindowCreateClient(id=str(item['values'][0]))
                except IndexError:
                    pass
            else:
                pass

        def right_click_menu(e):
            def delete_row():
                SQLite.del_row_Clients(str(self.table.set(row_id)['ID']))
                SQLite.del_row_Car_by_client(str(self.table.set(row_id)[_('Client')]))

                self.update_table()

            # create a popup menu
            row_id = self.table.identify('item', e.x, e.y)

            if row_id:
                self.table.selection_set(row_id)
                self.table.focus_set()
                self.table.focus(row_id)

                menu = Menu(self, tearoff=0)
                menu.add_command(label=_("Delete"), command=delete_row)
                menu.post(e.x_root, e.y_root)

                Label(self, height=8).grid(row=10, column=0, columnspan=100, sticky='ew')
            else:
                pass

        def show_car_table(e):
            # select row under mouse
            row_id = self.table.identify_row(e.y)

            if row_id:
                self.rowconfigure(9, {'minsize': 15})

                self.table.selection_set(row_id)

                # command for update
                def update_table_car():
                    row_del_car = table_car.get_children()

                    for row_t_car in row_del_car:
                        table_car.delete(row_t_car)

                    rows_ins_car = SQLite.sel_from_car(str(self.table.set(row_id)[_('Client')]))

                    for row_t_car in rows_ins_car:
                        table_car.insert('', END, values=tuple(row_t_car))

                headings_car = ('ID', _('Mark Model'), 'VIN', _('Client'),
                                _('Year of release'), _('Name'))

                rows_car = SQLite.sel_from_car(str(self.table.set(row_id)[_('Client')]))

                table_car = AGO.CreateTreeview(master=self, height=4, headings=headings_car,
                                               rows=rows_car, row=10, column=0, columnspan=100)

                table_car.column(_('Name'), anchor='w', width=300)

                def select_car(event):
                    item_car = table_car.item(table_car.selection())

                    row_id_car = table_car.identify('item', event.x, event.y)

                    if row_id_car:
                        try:
                            WCCar.WindowCreateCar(id=str(item_car['values'][0]))
                        except IndexError:
                            pass
                    else:
                        pass

                def right_click_menu_car(event):
                    def delete_row_car():
                        SQLite.del_row_Car_by_id(str(table_car.set(row_id_car)['ID']))

                        update_table_car()

                    # create a popup menu
                    row_id_car = table_car.identify('item', event.x, event.y)

                    if row_id_car:
                        table_car.selection_set(row_id_car)
                        table_car.focus_set()
                        table_car.focus(row_id_car)

                        menu = Menu(self, tearoff=0)
                        menu.add_command(label=_("Delete"), command=delete_row_car)
                        menu.post(event.x_root, event.y_root)
                    else:
                        pass

                table_car.bind("<Double-1>", select_car)

                table_car.bind("<Button-3>", right_click_menu_car)
            else:
                Label(self, height=8).grid(row=10, column=0, columnspan=100, sticky='ew')

        self.table.bind("<Double-1>", select)

        self.table.bind("<Button-3>", right_click_menu)

        self.table.bind("<1>", show_car_table)

        for col in headings:
            self.table.heading(col, text=col,
                               command=lambda _col=col: AF.treeview_sort_column(self.table, _col, False))

        self.table.grid(row=8, column=0, columnspan=100, sticky='ew')

        '''scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)'''
