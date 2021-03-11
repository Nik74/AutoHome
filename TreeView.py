# TreeView creates a tree list and output frames depending on the selected element in the tree

from tkinter import *
from tkinter import ttk
from Auxiliary import AuxiliaryFunctionsForTree as AFT, AuxiliaryGlobalObject as AGO
from Frames import FrameClients, FrameGoods


def create_tree_and_frames(frame, master=None):
    canvas_tree = Canvas(frame, width=100)

    # height = 48
    tree_view = ttk.Treeview(canvas_tree, height=int(AGO.height_window / 22.5),
                             selectmode='browse')

    tree_view.heading('#0', text='AutoHome', anchor='w')

    # minwidth = 250
    tree_view.column("#0", width=250)

    '''def rec_canvas(event):
        canvas_tree.configure(scrollregion=canvas_tree.bbox('all'))'''

    result = AFT.add_list_to_tree_from_bd(tree_view)

    tree_view.item(result, open=True)

    '''scrollbar_tree = Scrollbar(frame, orient='horizontal')

    scrollbar_tree['command'] = tree_view.xview
    tree_view['xscrollcommand'] = scrollbar_tree.set

    canvas_tree.create_window((0, 0), window=tree_view, anchor="nw")

    tree_view.bind("<Configure>", rec_canvas)'''

    '''scrollbar_tree.pack(side='bottom', fill=X)
    tree_view.pack()'''

    tree_view.grid(row=0, column=0, sticky='ew')

    canvas_tree.grid(row=0, column=0, sticky='ew')
    # scrollbar_tree.grid(row=1, column=0, sticky='ew')

    # client frame
    frame_client = FrameClients.FrameClients(master=master)

    # goods frame
    frame_goods = FrameGoods.FrameGoods(master=master)

    def clicks(event):
        item = tree_view.identify('item', event.x, event.y)

        if item == 'Clients':
            AFT.pack_out(frame_client)
        else:
            frame_client.pack_forget()

        if item == 'Goods':
            AFT.pack_out(frame_goods)
        else:
            frame_goods.pack_forget()

        if item == '':
            try:
                tree_view.selection_remove(tree_view.selection()[0])
            except IndexError:
                pass

    tree_view.bind("<1>", clicks)


class TreeView(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        # pacx = 10, pady = 10
        self.pack(padx=int(AGO.width_window / 192), pady=int(AGO.height_window / 108),
                  side='left', fill=Y)

        create_tree_and_frames(self, master=master)
