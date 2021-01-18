# AppWindow creates an app window

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO
from win32api import GetSystemMetrics

import TreeView


path_logo_ico = 'img/logo.ico'

_ = AGO.t.gettext


class AppWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoHome")
        self.iconbitmap(path_logo_ico)
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

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?')):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)

        self.mainloop()
