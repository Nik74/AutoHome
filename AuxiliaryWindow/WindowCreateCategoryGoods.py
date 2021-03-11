from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctionsForTree as AFT, \
    AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreateCategoryGoodsGroup as WCCG, \
    WindowRenameCategoryGoodsGroup as WRCGG

import SQLite
import Logs


_ = AGO.t.gettext


class WindowCreateCategoryGoods(Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.master = parent

        self.grab_set()

        def grab():
            if self.grab_status() is None and \
                    len(self.winfo_children()) == 3:
                
                self.grab_set()

            self.after(1000, grab)

        self.after(1000, grab)

        self.title(_("Create category goods"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        def create_group():
            WCCG.WindowCreateCategoryGoodsGroup(parent_window=self)

        AGO.CreateButton(master=self, text=_('Create group'), row=0,
                         column=0, command=create_group)

        AGO.CreateButton(master=self, text=_('Update'), row=0,
                         column=1, command=self.update_table)

        self.tree_category_goods = CanvasCategoryGoods(master=self)

        # minsize: 10
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 108)})

        # minsize: 10
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 192)})

        self.grid_columnconfigure(2, weight=1)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)

    # command for button of update
    def update_table(self):
        for i in self.tree_category_goods.tree_goods.get_children():
            self.tree_category_goods.tree_goods.delete(i)

        AFT.add_list_goods_tree_from_bd(self.tree_category_goods.tree_goods)


# command for button of update
def update_table(table):
    row_del = table.get_children()

    for row in row_del:
        table.delete(row)

    AFT.add_list_goods_tree_from_bd(table)


# Canvas for category goods tree
class CanvasCategoryGoods(Canvas):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        '''def select(e):
            row_id = self.tree_goods.identify('item', e.x, e.y)

            if row_id:
                pass
            else:
                try:
                    self.tree_goods.selection_remove(self.tree_goods.selection()[0])
                except IndexError:
                    pass'''

        def right_click_menu(e):
            def delete_row():
                SQLite.del_rows_Category_goods_by_parent((self.tree_goods.identify('item', e.x, e.y),))

                update_table(self.tree_goods)

            def add_subgroup():
                WCCG.WindowCreateCategoryGoodsGroup(parent=self.tree_goods.identify('item', e.x, e.y),
                                                    parent_window=master)

            def rename_category():
                WRCGG.WindowRenameCategoryGoodsGroup(element=self.tree_goods.identify('item', e.x, e.y),
                                                     parent=master)

            # create a popup menu
            row_id = self.tree_goods.identify('item', e.x, e.y)

            if row_id:
                self.tree_goods.selection_set(row_id)
                self.tree_goods.focus_set()
                self.tree_goods.focus(row_id)

                menu = Menu(self, tearoff=0)

                menu.add_command(label=_("Add subgroup"), command=add_subgroup)
                menu.add_command(label=_("Rename"), command=rename_category)
                menu.add_command(label=_("Delete"), command=delete_row)

                menu.post(e.x_root, e.y_root)
            else:
                pass

        def bDown(event):
            tv = event.widget

            if tv.identify_row(event.y) not in tv.selection():
                tv.selection_set(tv.identify_row(event.y))

        def bUp(event):
            tv = event.widget

            if tv.identify_row(event.y) in tv.selection():
                tv.selection_set(tv.identify_row(event.y))

            category_tree = list(tv.get_children())

            cat = AF.aux_func()

            if len(cat) == len(category_tree):
                for i in range(0, len(category_tree) - 1):
                    if cat[i] != category_tree[i]:
                        SQLite.swap_rows_Category_goods(cat[i],
                                                        category_tree[i])

                    cat = AF.aux_func()
            else:
                Logs.logger.error("The number of rows in sqlite and "
                                  "the category tree is different")

        def bMove(event):
            tv = event.widget

            try:
                item_iid = tv.selection()[0]
                parent_iid = tv.parent(item_iid)

                if parent_iid:
                    pass
                else:
                    moveto = tv.index(tv.identify_row(event.y))

                    for s in tv.selection():
                        # tv.move(s, tv.identify_row(event.y), moveto)
                        tv.move(s, '', moveto)
            except IndexError:
                pass

        self.tree_goods = ttk.Treeview(self, selectmode='browse')

        self.tree_goods.heading('#0', text=_('Categories goods'), anchor='w')

        self.tree_goods.column("#0", width=310)

        AFT.add_list_goods_tree_from_bd(self.tree_goods)

        #self.tree_goods.bind('<1>', select)
        self.tree_goods.bind("<Button-3>", right_click_menu)
        self.tree_goods.bind("<ButtonPress-1>", bDown)
        self.tree_goods.bind("<ButtonRelease-1>", bUp, add='+')
        self.tree_goods.bind("<B1-Motion>", bMove, add='+')

        self.tree_goods.grid(row=0, column=0, sticky='ew')

        self.grid(row=2, column=0, sticky='ew', columnspan=3)
