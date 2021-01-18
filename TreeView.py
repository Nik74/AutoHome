# TreeView creates a tree list and output frames depending on the selected element in the tree

from tkinter import *
from tkinter import ttk
from Auxiliary import AuxiliaryFunctionsForTree as AFT, AuxiliaryGlobalObject as AGO
from Frames import FrameClients


def create_tree_and_frames(frame, master=None):
    tree_view = ttk.Treeview(frame, height=AGO.height_program, selectmode='browse')

    tree_view.heading('#0', text='AutoHome', anchor='w')

    # minwidth = 250
    tree_view.column("#0", width=int(AGO.width_program / 3.35),
                     minwidth="{}".format(250))

    result = AFT.add_list_to_tree_from_bd(tree_view)

    tree_view.item(result, open=True)

    scrollbar_tree = Scrollbar(frame, orient='horizontal')

    scrollbar_tree['command'] = tree_view.xview
    tree_view['xscrollcommand'] = scrollbar_tree.set

    scrollbar_tree.pack(side='bottom', fill=X)
    tree_view.pack()

    frame_client = FrameClients.FrameClients(master=master)

    def clicks(event):
        item = tree_view.identify('item', event.x, event.y)

        if item == 'Clients':
            AFT.pack_out(frame_client)
        else:
            AFT.hide_frame(frame_client)

        if item == 'Goods':
            print('dsf')

    tree_view.bind("<1>", clicks)


class TreeView(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        # pacx = 10, pady = 10
        self.pack(padx=int(AGO.width_window / 192), pady=int(AGO.height_window / 108), side='left', fill=Y)
        create_tree_and_frames(self, master=master)
