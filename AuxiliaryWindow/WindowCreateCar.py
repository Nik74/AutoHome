# Window for create car

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO

import SQLite
import datetime

_ = AGO.t.gettext


# frame containing information on car
def frame_inf(frame, id_car):
    frame_inform = Frame(frame)

    item = ['' for _ in range(0, 17)]

    if id_car is not None:
        sel_car = SQLite.sel_from_car_all(id_car)

        if sel_car is not None:
            item = sel_car[0]

    inf_car = dict()

    # label mark
    AGO.CreateLabel(master=frame_inform, text=_('Mark'),
                    row=0, column=0, sticky='w')

    mark = []

    for m in SQLite.sel_mark_from_car():
        if m != ('',):
            mark.append('.'.join(m))

    def upd_model(event):
        model = []

        for m in SQLite.sel_model_from_car_by_mark(inf_car['Mark'].get()):
            if m != ('',):
                model.append('.'.join(m))

        # combobox model
        inf_car['Model'] = AGO.AutocompleteCombobox(master=frame_inform, row=0, column=3,
                                                    list_box=model, item=item[2],
                                                    columnspan=4)
    # combobox mark
    inf_car['Mark'] = AGO.AutocompleteCombobox(master=frame_inform, row=0, column=1,
                                               list_box=mark, item=item[1],
                                               events="<Tab>", command=upd_model)
    # label model
    AGO.CreateLabel(master=frame_inform, text=_('Model'), row=0,
                    column=2, sticky='w')

    model = []

    for m in SQLite.sel_model_from_car_by_mark(inf_car['Mark'].get()):
        if m != ('',):
            model.append('.'.join(m))

    # combobox model
    inf_car['Model'] = AGO.AutocompleteCombobox(master=frame_inform, row=0, column=3,
                                                list_box=model, item=item[2],
                                                columnspan=4)
    # label license plate number
    AGO.CreateLabel(master=frame_inform, text=_('License plate number'),
                    row=0, column=7, sticky='w')

    # entry license plate number
    inf_car['License_plate_number'] = AGO.CreateEntry(master=frame_inform, item=item[3],
                                                      row=0, column=8, columnspan=2).text
    # label vin
    AGO.CreateLabel(master=frame_inform, text='VIN', row=0, column=10, sticky='w')

    # entry vin
    inf_car['VIN'] = AGO.CreateEntry(master=frame_inform, item=item[4], row=0,
                                     column=11).text
    # minsize: 10
    frame_inform.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

    # label year release
    AGO.CreateLabel(master=frame_inform, text=_('Year of release'), row=2,
                    column=0, sticky='w')

    # entry year release
    inf_car['Year_release'] = AGO.CreateEntry(master=frame_inform, item=item[5],
                                              row=2, column=1).text
    # label engine
    AGO.CreateLabel(master=frame_inform, text=_('Engine'), row=2, column=2, sticky='w')

    # entry engine
    inf_car['Engine'] = AGO.CreateEntry(master=frame_inform, item=item[6],
                                        row=2, column=3, columnspan=4).text
    # label gearbox
    AGO.CreateLabel(master=frame_inform, text=_('Gearbox'), row=2, column=7,
                    sticky='w')

    gearbox = []

    for g in SQLite.sel_gearbox_from_car():
        if g != ('',):
            gearbox.append('.'.join(g))

    # combobox gearbox
    inf_car['Gearbox'] = AGO.AutocompleteCombobox(master=frame_inform, row=2, column=8,
                                                  list_box=gearbox, item=item[7],
                                                  columnspan=2)
    # label body car
    AGO.CreateLabel(master=frame_inform, text=_('Body car'), row=2, column=10, sticky='w')

    body_car = []

    for bc in SQLite.sel_body_car_from_car():
        if bc != ('',):
            body_car.append('.'.join(bc))

    # combobox body car
    inf_car['Body_car'] = AGO.AutocompleteCombobox(master=frame_inform, row=2, column=11,
                                                   list_box=body_car, item=item[8])
    # minsize: 10
    frame_inform.rowconfigure(3, {'minsize': int(AGO.height_window / 108)})

    # label machine drive
    AGO.CreateLabel(master=frame_inform, text=_('Machine drive'), row=4, column=0,
                    sticky='w')

    machine_drive = []

    for md in SQLite.sel_machine_drive_from_car():
        if md != ('',):
            machine_drive.append('.'.join(md))

    # combobox machine drive
    inf_car['Machine drive'] = AGO.AutocompleteCombobox(master=frame_inform, row=4, column=1,
                                                        list_box=machine_drive, item=item[9],
                                                        columnspan=4)
    # label right hand drive
    AGO.CreateLabel(master=frame_inform, text=_('Right hand drive'), row=4, column=5,
                    sticky='w')

    # checkbutton right hand drive
    inf_car['Right_hand_drive'] = AGO.CreateCheckbutton(master=frame_inform, item=item[10],
                                                        row=4, column=6).sel
    # label unit mileage measurement
    AGO.CreateLabel(master=frame_inform, text=_('The unit of measure of the mileage'),
                    row=4, column=7, columnspan=2, sticky='w')

    unit_mileage_measurement = []

    for umm in SQLite.sel_unit_mileage_measurement_from_car():
        if umm != ('',):
            unit_mileage_measurement.append('.'.join(umm))

    # combobox unit mileage measurement
    inf_car['Unit_mileage_measurement'] = AGO.AutocompleteCombobox(master=frame_inform, row=4, column=9,
                                                                   list_box=unit_mileage_measurement,
                                                                   item=item[11])
    # label color
    AGO.CreateLabel(master=frame_inform, text=_('Color'), row=4, column=10, sticky='w')

    color = []

    for c in SQLite.sel_color_from_car():
        if c != ('',):
            color.append('.'.join(c))

    def resize_func(event):
        new_len = len(inf_car['Color'].get())
        inf_car['Color'].configure(width=new_len + 2)

    # combobox color
    inf_car['Color'] = AGO.AutocompleteCombobox(master=frame_inform, row=4, column=11,
                                                list_box=color, item=item[12],
                                                events="<<ComboboxSelected>>",
                                                command=resize_func)
    # minsize: 10
    frame_inform.rowconfigure(5, {'minsize': int(AGO.height_window / 108)})

    # label body number
    AGO.CreateLabel(master=frame_inform, text=_('Body number'), row=6, column=0, sticky='w')

    # entry body number
    inf_car['Body_number'] = AGO.CreateEntry(master=frame_inform, item=item[13], row=6,
                                             column=1, columnspan=6).text
    # label engine number
    AGO.CreateLabel(master=frame_inform, text=_('Engine number'), row=6, column=7,
                    sticky='w')

    # entry engine number
    inf_car['Engine_number'] = AGO.CreateEntry(master=frame_inform, item=item[14],
                                               row=6, column=8, columnspan=4).text
    # minsize: 10
    frame_inform.rowconfigure(7, {'minsize': int(AGO.height_window / 108)})

    # label client
    AGO.CreateLabel(master=frame_inform, text=_('Client'), row=8, column=0, sticky='w')

    client = []

    for c in SQLite.sel_client_from_clients():
        if c != ('',):
            client.append('.'.join(c))

    # combobox client
    inf_car['Client'] = AGO.AutocompleteCombobox(master=frame_inform, row=8, column=1,
                                                 list_box=client, item=item[15],
                                                 columnspan=9)
    # label created
    AGO.CreateLabel(master=frame_inform, text=_('Created'), row=8, column=10,
                    sticky='w')

    date_now = datetime.datetime.now()

    if item[16] == '':
        item[16] = date_now.strftime('%d.%m.%Y %H:%M:%S')

    # entry created
    inf_car['Created'] = AGO.CreateEntry(master=frame_inform, item=item[16],
                                         row=8, column=11).text

    frame_inform.grid(row=3, column=1, sticky='w')

    return inf_car


class WindowCreateCar(Toplevel):
    def __init__(self, id=None, parent=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Create car"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        # minsize: 10
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

        # minsize: 10
        self.rowconfigure(0, {'minsize': int(AGO.height_window / 108)})

        # Save client
        def save_client():
            inf_car = list()

            check_lic_plate_num = SQLite.sel_license_plate_number_from_car()

            if car.get('Mark').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "Mark" field is not completed'),
                                       parent=self)
                return 0

            if tuple([car.get('Client').get()]) not in SQLite.sel_client_from_clients():
                messagebox.showwarning(_("Warning"),
                                       _('Such a client does not exist'),
                                       parent=self)
                return 0

            if car.get('License_plate_number').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "License plate number" field is not completed'),
                                       parent=self)
                return 0

            for i in car.values():
                if type(i) is str:
                    inf_car.append(i)
                else:
                    inf_car.append(i.get())

            if id is not None:
                inf_car.append(id)

                SQLite.upd_Car(inf_car)
            else:
                if (car.get('License_plate_number').get(),) in check_lic_plate_num:
                    inf_car.append(car.get('License_plate_number').get())

                    SQLite.upd_Car_by_license_plate_number(inf_car)
                else:
                    SQLite.ins_Car(inf_car)

        # Save and exit
        def save_client_and_exit():
            pass
            err = save_client()

            if err is None:
                self.destroy()

        car = dict()

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

        car = frame_inf(self, id_car=id)

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
