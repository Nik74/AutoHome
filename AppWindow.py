# AppWindow creates an app window

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO
from win32api import GetSystemMetrics

import TreeView
import os
import shutil

_ = AGO.t.gettext


class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("AutoHome")

        self.iconbitmap(AGO.path_logo_ico)

        self.wm_state('zoomed')

        # Setting the location of the application window relative to the user's screen resolution
        w_center = int((GetSystemMetrics(0) - AGO.width_program) / 2)
        h_center = int((GetSystemMetrics(1) - AGO.height_program) / 2)

        # Creating an application window
        self.geometry("{}x{}+{}+{}".format(AGO.width_program, AGO.height_program,
                                           w_center, h_center))
        style = ttk.Style()
        style.theme_use('vista')

        TreeView.TreeView(master=self)

        def back_up_bd():
            if os.path.exists("SQLiteDB/AutoHome_backup3.db"):
                if os.path.exists("SQLiteDB/AutoHome_backup4.db"):
                    os.remove("SQLiteDB/AutoHome_backup4.db")

                os.rename("SQLiteDB/AutoHome_backup3.db",
                          "SQLiteDB/AutoHome_backup4.db")

            if os.path.exists("SQLiteDB/AutoHome_backup2.db"):
                os.rename("SQLiteDB/AutoHome_backup2.db",
                          "SQLiteDB/AutoHome_backup3.db")

            if os.path.exists("SQLiteDB/AutoHome_backup1.db"):
                os.rename("SQLiteDB/AutoHome_backup1.db",
                          "SQLiteDB/AutoHome_backup2.db")

            if os.path.exists("SQLiteDB/AutoHome_backup.db"):
                os.rename("SQLiteDB/AutoHome_backup.db",
                          "SQLiteDB/AutoHome_backup1.db")

            if os.path.exists("SQLiteDB/AutoHome.db"):
                shutil.copyfile("SQLiteDB/AutoHome.db", "SQLiteDB/AutoHome_backup.db")

            self.after(1800000, back_up_bd)

        self.after(1800000, back_up_bd)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?')):
                back_up_bd()

                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)

        self.mainloop()
