# Window for create client

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreateCar as WCCar

import SQLite

path_logo_ico = 'img/logo.ico'

_ = AGO.t.gettext

category = (_('Constant'), _('Organization'), _('Standard'), 'VIP')
source = (_('Search network'), 'Instagram', 'Vkontakte', 'OK', _('Electronic map'), _('Friends/Familiar'),
          _('Internet'), _('Signboard'), _('Familiar'), _('Mailing'), 'E-mail', _('Other'), _('Not'))


# frame for communication
def frame_communication(frame, item):
    frame_comm = Frame(frame, highlightbackground="black",
                       highlightcolor='black', highlightthickness=1, bd=0)

    inf_communication = dict()

    # label communication
    AGO.CreateLabel(master=frame_comm, text=_('Communication'), bg='#cac7c6', anchor='w', row=0,
                    column=0, columnspan=13)

    # minsize: 10
    frame_comm.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})
    frame_comm.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

    # label phone number
    AGO.CreateLabel(master=frame_comm, text=_('Phone number'), row=2, column=1, sticky='w')

    # entry phone number
    inf_communication['phone_number'] = AGO.CreateEntry(master=frame_comm,
                                                        item=item[7], row=2, column=2).text
    # label other_phone_number
    AGO.CreateLabel(master=frame_comm, text=_('Other phone number'), row=2, column=3, sticky='w')

    # entry other phone number
    inf_communication['other_phone_number'] = AGO.CreateEntry(master=frame_comm, item=item[8],
                                                              row=2, column=4).text
    # label e-mail
    AGO.CreateLabel(master=frame_comm, text='E-mail', row=2, column=5, sticky='w')

    # entry e-mail
    inf_communication['e_mail'] = AGO.CreateEntry(master=frame_comm, item=item[9], row=2,
                                                  column=6, columnspan=6).text
    # minsize: 10
    frame_comm.rowconfigure(3, {'minsize': int(AGO.height_window / 108)})

    # label address
    AGO.CreateLabel(master=frame_comm, text=_('Address'), row=4, column=1, sticky='w')

    # entry address
    inf_communication['address'] = AGO.CreateEntry(master=frame_comm, item=item[10], row=4,
                                                   column=2, columnspan=10).text
    # minsize: 10
    frame_comm.rowconfigure(5, {'minsize': int(AGO.height_window / 108)})

    # label site
    AGO.CreateLabel(master=frame_comm, text=_('Site'), row=6, column=1, sticky='w')

    # entry site
    inf_communication['site'] = AGO.CreateEntry(master=frame_comm, item=item[11], row=6, column=2).text

    # label social networking
    AGO.CreateLabel(master=frame_comm, text=_('Social networking'), row=6, column=3, sticky='w')

    # entry social networking
    inf_communication['social_networking'] = AGO.CreateEntry(master=frame_comm, item=item[12],
                                                             row=6, column=4).text
    # label problem client
    AGO.CreateLabel(master=frame_comm, text=_('Problem client'), row=6, column=5,
                    columnspan=2, sticky='w')

    # checkbutton problem client
    inf_communication['problem_client'] = AGO.CreateCheckbutton(master=frame_comm, item=item[13],
                                                                row=6, column=7).sel
    # label send sms
    AGO.CreateLabel(master=frame_comm, text=_('Send SMS'), row=6, column=8, sticky='w')

    # checkbutton send sms
    inf_communication['send_sms'] = AGO.CreateCheckbutton(master=frame_comm, item=item[14],
                                                          row=6, column=9).sel
    # label send e-mail
    AGO.CreateLabel(master=frame_comm, text=_('Send E-Mail'), row=6, column=10, sticky='w')

    # checkbutton send e-mail
    inf_communication['send_e_mail'] = AGO.CreateCheckbutton(master=frame_comm, item=item[15],
                                                             row=6, column=11).sel
    # minsize: 10
    frame_comm.rowconfigure(7, {'minsize': int(AGO.height_window / 108)})
    frame_comm.columnconfigure(12, {'minsize': int(AGO.width_window / 192)})

    frame_comm.grid_columnconfigure(2, weight=1)
    frame_comm.grid_columnconfigure(4, weight=1)

    frame_comm.grid(row=4, column=0, columnspan=8, sticky='ew')

    return inf_communication


# frame for codes
def frame_codes(frame, item):
    frame_code = Frame(frame, highlightbackground='gray',
                       highlightcolor='black', highlightthickness=1, bd=0)

    inf_codes = dict()

    # label codes
    AGO.CreateLabel(master=frame_code, text=_('Codes'), bg='#cac7c6', anchor='w',
                    row=0, column=0, columnspan=6)
    # minsize: 10
    frame_code.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

    # minsize: 10
    frame_code.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

    # label inn
    AGO.CreateLabel(master=frame_code, text=_('INN'), row=2, column=1, sticky='w')

    # entry inn
    inf_codes['inn'] = AGO.CreateEntry(master=frame_code, item=item[16], row=2, column=2).text

    # label kpp
    AGO.CreateLabel(master=frame_code, text=_('KPP'), row=2, column=3, sticky='w')

    # entry kpp
    inf_codes['kpp'] = AGO.CreateEntry(master=frame_code, item=item[17], row=2, column=4).text

    # minsize:10
    frame_code.rowconfigure(3, {'minsize': int(AGO.height_window / 108)})

    # label ogrn
    AGO.CreateLabel(master=frame_code, text=_('OGRN'), row=4, column=1, sticky='w')

    # entry ogrn
    inf_codes['ogrn'] = AGO.CreateEntry(master=frame_code, item=item[18], row=4, column=2).text

    # label okpo
    AGO.CreateLabel(master=frame_code, text=_('OKPO'), row=4, column=3, sticky='w')

    # entry okpo
    inf_codes['okpo'] = AGO.CreateEntry(master=frame_code, item=item[19], row=4, column=4).text

    # minsize: 10
    frame_code.rowconfigure(5, {'minsize': int(AGO.height_window / 108)})

    # label okved
    AGO.CreateLabel(master=frame_code, text=_('OKVED'), row=6, column=1, sticky='w')

    # entry okved
    inf_codes['okved'] = AGO.CreateEntry(master=frame_code, item=item[20], row=6, column=2).text

    # label oktmo
    AGO.CreateLabel(master=frame_code, text=_('OKTMO'), row=6, column=3, sticky='w')

    # entry oktmo
    inf_codes['oktmo'] = AGO.CreateEntry(master=frame_code, item=item[21], row=6, column=4).text

    # minsize: 10
    frame_code.columnconfigure(5, {'minsize': int(AGO.width_window / 192)})

    # minsize: 10
    frame_code.rowconfigure(7, {'minsize': int(AGO.height_window / 108)})

    frame_code.grid_columnconfigure(2, weight=1)
    frame_code.grid_columnconfigure(4, weight=1)

    frame_code.grid(row=1, column=1, sticky='ew')

    return inf_codes


# frame for bank
def frame_bank(frame, item):
    frame_bk = Frame(frame, highlightbackground='gray',
                     highlightcolor='black', highlightthickness=1, bd=0)

    inf_bank = dict()

    # label bank (stripe)
    AGO.CreateLabel(master=frame_bk, text=_('Bank'), bg='#cac7c6', anchor='w',
                    row=0, column=0, columnspan=6)
    # minsize: 10
    frame_bk.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

    # minsize: 10
    frame_bk.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

    # label bank
    AGO.CreateLabel(master=frame_bk, text=_('Bank'), row=2, column=1, sticky='w')

    # entry bank
    inf_bank['bank'] = AGO.CreateEntry(master=frame_bk, item=item[22], row=2,
                                       column=2, columnspan=3).text
    # minsize: 10
    frame_bk.rowconfigure(3, {'minsize': int(AGO.height_window / 108)})

    # label bik
    AGO.CreateLabel(master=frame_bk, text=_('BIK'), row=4, column=1, sticky='w')

    # entry bik
    inf_bank['bik'] = AGO.CreateEntry(master=frame_bk, item=item[23], row=4,
                                      column=2, columnspan=3).text
    # minsize: 10
    frame_bk.rowconfigure(5, {'minsize': int(AGO.height_window / 108)})

    # label r/s
    AGO.CreateLabel(master=frame_bk, text=_('R/S'), row=6, column=1, sticky='w')

    # entry r/s
    inf_bank['r_s'] = AGO.CreateEntry(master=frame_bk, item=item[24], row=6, column=2).text

    # label corr. acc
    AGO.CreateLabel(master=frame_bk, text=_('Correct account'), row=6, column=3, sticky='w')

    # entry corr. acc
    inf_bank['corr_acc'] = AGO.CreateEntry(master=frame_bk, item=item[25], row=6, column=4).text

    # minsize: 10
    frame_bk.columnconfigure(5, {'minsize': int(AGO.width_window / 192)})

    # minsize: 10
    frame_bk.rowconfigure(7, {'minsize': int(AGO.height_window / 108)})

    frame_bk.grid_columnconfigure(2, weight=1)
    frame_bk.grid_columnconfigure(4, weight=1)

    frame_bk.grid(row=1, column=3, sticky='ew')

    return inf_bank


# frame for legal entity
def frame_legal_entity(frame, item):
    frame_legal_ent = Frame(frame, highlightbackground="black",
                            highlightcolor='black', highlightthickness=1, bd=0)

    inf_legal_entity = dict()

    # minsize: 10
    frame_legal_ent.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

    # label legal entity
    AGO.CreateLabel(master=frame_legal_ent, text=_('Legal entity'), bg='#cac7c6', anchor='w',
                    row=0, column=0, columnspan=5)

    # //////////////////////////////////////////////////FRAME_CODES\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
    inf_legal_entity.update(frame_codes(frame_legal_ent, item))
    # ///////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #

    # minsize: 10
    frame_legal_ent.columnconfigure(2, {'minsize': int(AGO.width_window / 192)})

    # //////////////////////////////////////////////////FRAME_BANK\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
    inf_legal_entity.update(frame_bank(frame_legal_ent, item))
    # ///////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #

    # minsize: 10
    frame_legal_ent.columnconfigure(4, {'minsize': int(AGO.width_window / 192)})

    # minsize: 15
    frame_legal_ent.rowconfigure(2, {'minsize': int(AGO.height_window / 72)})

    frame_legal_ent.grid_columnconfigure(1, weight=1)
    frame_legal_ent.grid_columnconfigure(3, weight=1)

    frame_legal_ent.grid(row=7, column=0, columnspan=8, sticky='ew')

    return inf_legal_entity


# frame containing information on client
def frame_inf(frame, id_client):
    frame_inform = Frame(frame)

    item = ['' for _ in range(0, 27)]

    if id_client is not None:
        sel_client = SQLite.sel_from_clients_all(id_client)

        if sel_client is not None:
            item = sel_client[0]

    inf_client = dict()

    # label client
    AGO.CreateLabel(master=frame_inform, text=_('Client'),
                    row=0, column=0, sticky='w')

    # entry client
    inf_client['client'] = AGO.CreateEntry(master=frame_inform, item=item[1], row=0,
                                           column=1, columnspan=5).text
    # label type client
    AGO.CreateLabel(master=frame_inform, text=_('Type client'), row=0, column=6, sticky='w')

    # entry type client
    inf_client['type_client'] = AGO.CreateEntry(master=frame_inform, item=item[2],
                                                row=0, column=7).text
    # minsize: 10
    frame_inform.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

    # label category
    AGO.CreateLabel(master=frame_inform, text=_('Category'), row=2, column=0, sticky='w')

    # combobox category
    inf_client['category'] = AGO.CreateCombobox(master=frame_inform, list_box=category,
                                                item=item[3], row=2, column=1)
    # label source
    AGO.CreateLabel(master=frame_inform, text=_('Source'), row=2, column=2, sticky='w')

    # combobox source
    inf_client['source'] = AGO.CreateCombobox(master=frame_inform, list_box=source,
                                              item=item[4], row=2, column=3)
    # label discount on works
    AGO.CreateLabel(master=frame_inform, text=_('Discount on works %'), row=2,
                    column=4, sticky='w')

    # entry discount on works
    inf_client['discount_on_works'] = AGO.CreateEntry(master=frame_inform, item=item[5], row=2,
                                                      column=5).text
    # label discount on products
    AGO.CreateLabel(master=frame_inform, text=_('Discount on products %'), row=2,
                    column=6, sticky='w')

    # entry discount on products
    inf_client['discount_on_products'] = AGO.CreateEntry(master=frame_inform, item=item[6],
                                                         row=2, column=7).text
    # minsize: 20
    frame_inform.rowconfigure(3, {'minsize': int(AGO.height_window / 54)})

    # //////////////////////////////////////////////////FRAME_COMMUNICATION\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
    inf_client.update(frame_communication(frame_inform, item))
    # ///////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #

    # minsize: 20
    frame_inform.rowconfigure(5, {'minsize': int(AGO.height_window / 54)})

    # if frame_legal_entity not show
    inf_client['inn'] = ''
    inf_client['kpp'] = ''
    inf_client['ogrn'] = ''
    inf_client['okpo'] = ''
    inf_client['okved'] = ''
    inf_client['oktmo'] = ''
    inf_client['bank'] = ''
    inf_client['bik'] = ''
    inf_client['r_s'] = ''
    inf_client['corr_acc'] = ''

    def show_frame_legal_entity():
        # //////////////////////////////////////////////////FRAME_LEGAL_ENTITY\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
        inf_client.update(frame_legal_entity(frame_inform, item))
        # ///////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #

    if item[16] == '':
        AGO.CreateButton(master=frame_inform, text=_('Legal entity'), row=6, column=0,
                         command=show_frame_legal_entity, sticky='w')
    else:
        inf_client.update(frame_legal_entity(frame_inform, item))

    # minsize: 20
    frame_inform.rowconfigure(8, {'minsize': int(AGO.height_window / 54)})

    # label note
    AGO.CreateLabel(master=frame_inform, text=_('Notes'), row=9, column=0, sticky='w')

    # text note
    inf_client['note'] = AGO.CreateText(master=frame_inform, height=int(AGO.height_window / 108),
                                        item=item[26], row=10, column=0, columnspan=8, sticky='ew')
    for k in [1, 3, 5, 7]:
        frame_inform.grid_columnconfigure(k, weight=1)

    frame_inform.grid(row=3, column=1, sticky='ew')

    return inf_client


# frame for all information: car, orders, product, payments and etc.
def frame_all_inf(frame, client):
    frame_all = Frame(frame, highlightbackground="black",
                      highlightcolor='black', highlightthickness=1, bd=0)

    # minsize: 10
    frame_all.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

    # select table Car
    def show_table_car():
        # command for update
        def update_table():
            row_del = table.get_children()

            for row_t in row_del:
                table.delete(row_t)

            rows_ins = SQLite.sel_from_car(client[0][0])

            for row_t in rows_ins:
                table.insert('', END, values=tuple(row_t))

        headings = ('ID', _('Mark Model'), 'VIN', _('Client'),
                    _('Year of release'), _('Name'))

        rows = SQLite.sel_from_car(client[0][0])

        table = AGO.CreateTreeview(master=frame_all, height=4, headings=headings,
                                   rows=rows, row=2, column=1, columnspan=100)

        table.column(_('Name'), anchor='w', width=300)

        def select(e):
            item = table.item(table.selection())

            row_id = table.identify('item', e.x, e.y)

            if row_id:
                try:
                    WCCar.WindowCreateCar(id=str(item['values'][0]))
                except IndexError:
                    pass
            else:
                pass

        def right_click_menu(e):
            def delete_row():
                SQLite.del_row_Car_by_id(str(table.set(row_id)['ID']))

                update_table()

            # create a popup menu
            row_id = table.identify('item', e.x, e.y)

            if row_id:
                table.selection_set(row_id)
                table.focus_set()
                table.focus(row_id)

                menu = Menu(frame_all, tearoff=0)
                menu.add_command(label=_("Delete"), command=delete_row)
                menu.post(e.x_root, e.y_root)
            else:
                pass

        table.bind("<Double-1>", select)

        table.bind("<Button-3>", right_click_menu)

    # button car
    AGO.CreateButton(master=frame_all, text=_('Cars'), row=0, column=1,
                     bg='red', sticky='w')

    # button order
    ''' AGO.CreateButton(master=frame_all, text=_('Orders'), bg='red', row=0, column=2)

    # button sale goods
    AGO.CreateButton(master=frame_all, text=_('Sale of goods'), bg='red', row=0, column=3)

    # button product reserve
    AGO.CreateButton(master=frame_all, text=_('Products reserves'), bg='red', row=0, column=4)

    # button payments
    AGO.CreateButton(master=frame_all, text=_('Payments'), bg='red', row=0, column=5)'''

    # minsize: 10
    frame_all.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

    show_table_car()

    frame_all.columnconfigure(1001, {'minsize': 5})

    # minsize: 10
    frame_all.rowconfigure(4, {'minsize': int(AGO.height_window / 108)})

    frame_all.grid_columnconfigure(1, weight=1)

    frame_all.grid(row=5, column=1, sticky='ew')


class WindowCreateClient(Toplevel):
    def __init__(self, id=None):
        super().__init__()
        self.title(_("Create client"))
        self.iconbitmap(path_logo_ico)
        self.wm_state('zoomed')

        style = ttk.Style()
        style.theme_use('vista')

        # minsize: 10
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

        # minsize: 10
        self.rowconfigure(0, {'minsize': int(AGO.height_window / 108)})

        # Save client
        def save_client():
            inf_client = list()

            if client.get('client').get() == '':
                messagebox.showwarning(_("Warning"), _('The "client" field is not completed'),
                                       parent=self)

                return 0

            if len(client.get('phone_number').get()) > 12 or \
                    len(client.get('other_phone_number').get()) > 12:
                messagebox.showwarning(_("Warning"), _('Phone number length error'),
                                       parent=self)

                return 0

            for i in client.values():
                if type(i) is AGO.CreateText:
                    if i.get(1.0, END) != '\n':
                        inf_client.append(i.get(1.0, END))
                    else:
                        inf_client.append('')
                elif type(i) is str:
                    inf_client.append(i)
                else:
                    inf_client.append(i.get())

            if id is not None:
                inf_client.append(id)

                SQLite.upd_Clients(inf_client)
            else:
                SQLite.ins_Client(inf_client)

        # Save and exit
        def save_client_and_exit():
            err = save_client()

            if err is None:
                self.destroy()

        client = dict()

        frame_but = Frame(self)

        # button save exit
        AGO.CreateButton(master=frame_but, text=_("Save and exit"),
                         command=save_client_and_exit, row=0, column=0)

        # button save
        AGO.CreateButton(master=frame_but, text=_("Save"),
                         command=save_client, row=0, column=1)

        frame_but.grid(row=1, column=1, sticky='w')

        # minsize: 5
        self.rowconfigure(2, {'minsize': int(AGO.height_window / 216)})

        client = frame_inf(self, id_client=id)

        # minsize: 10
        self.rowconfigure(4, {'minsize': int(AGO.height_window / 108)})

        # minsize: 10
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 192)})

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)

        self.grid_columnconfigure(1, weight=1)

        if id is not None:
            frame_all_inf(self, client=SQLite.sel_client_from_clients_by_id(id))
