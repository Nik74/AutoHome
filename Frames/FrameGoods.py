# The output of the functionality for the tab Goods

from tkinter import *
from tkinter import ttk

from Auxiliary import AuxiliaryGlobalObject as AGO, AuxiliaryFunctionsForTree as AFT, \
    AuxiliaryFunctions as AF
from AuxiliaryWindow import WindowCreateCategoryGoods as WCCG, WindowCreateGoods as WCG, \
    WindowPrintingOnPrint as WPOP

import Logs
import SQLite

_ = AGO.t.gettext


# main frame on goods
class FrameGoods(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # minsize: 15
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 72)})

        table_goods = FrameTableGoods(master=self).canvas_table_goods.table_goods

        tree_goods = FrameGoodsTree(master=self, table_goods=table_goods).category_tree

        CanvasButtonTop(master=self, tree_goods=tree_goods, table_goods=table_goods)

        # minsize: 15
        self.columnconfigure(1, {'minsize': int(AGO.width_window / 128)})
        self.columnconfigure(3, {'minsize': int(AGO.width_window / 128)})

        self.grid_columnconfigure(3, weight=2)


# command for button of update
def update_table(table, item):
    row_del = table.get_children()

    for row in row_del:
        table.delete(row)

    rows_ins = SQLite.sel_from_goods_by_category(item)

    for row in rows_ins:
        # if remains < minimum_balance, then row color - red
        if row[4] < row[7]:
            table.insert('', END, values=row, tags=('red',))
        else:
            table.insert('', END, values=row)


# Canvas for button on top
class CanvasButtonTop(Canvas):
    def __init__(self, master=None, tree_goods=None, table_goods=None):
        super().__init__(master)
        self.master = master

        self.button_top(tree_goods, table_goods, master.master)

        self.grid(row=0, column=0, columnspan=3, sticky='ew')

    def button_top(self, tree_goods, table_goods, master):
        def upd_table_goods():
            if (tree_goods is not None) and (table_goods is not None):
                update_table(table_goods, tree_goods.item)

        def create_product():
            WCG.WindowCreateGoods(category=tree_goods.item,
                                  parent=master)

        def print_product():
            WPOP.WindowPrintingOnPrint(category=tree_goods.item,
                                       parent=master)

        # button update
        AGO.CreateButton(master=self, text=_('Update'), row=0, column=0,
                         command=upd_table_goods)

        # button print product label
        AGO.CreateButton(master=self, text=_('Print Product label'), row=0,
                         column=1, command=print_product)

        # button create a product
        AGO.CreateButton(master=self, text=_('Create a product'), row=0,
                         column=2, command=create_product)

        # button open a card
        AGO.CreateButton(master=self, text=_('Open a card'), row=0,
                         column=3, bg='red')


# Frame for goods tree
class FrameGoodsTree(Canvas):
    def __init__(self, master=None, table_goods=None):
        super().__init__(master)
        self.master = master
        self.config(highlightthickness=0, bd=0)

        def create_category_goods():
            WCCG.WindowCreateCategoryGoods(parent=master.master)

        def update_category_tree():
            for i in self.category_tree.tree_goods.get_children():
                self.category_tree.tree_goods.delete(i)

            AFT.add_list_goods_tree_from_bd(self.category_tree.tree_goods)

        # button for setting up goods tree
        AGO.CreateButton(master=self, text=_('Customization'), row=0, column=0,
                         command=create_category_goods)

        AGO.CreateButton(master=self, text=_('Update categories goods'), row=0, column=1,
                         command=update_category_tree)

        # minsize: 5
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # minsize: 5
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 384)})

        self.grid_columnconfigure(2, weight=1)

        self.category_tree = CanvasGoodsTree(master=self, table_goods=table_goods)

        self.grid(row=2, column=0, sticky='ew')


# Canvas for goods tree
class CanvasGoodsTree(Canvas):
    def __init__(self, master=None, table_goods=None):
        super().__init__(master)
        self.master = master

        self.config(highlightthickness=0, bd=0)

        self.item = ''

        # width = 300, height = 830
        self.config(width=int(AGO.width_window / 6.4),
                    height=int(AGO.height_window / 1.301204819277108))

        def rec_canvas(event):
            self.configure(scrollregion=self.bbox('all'))

        '''def clicks(event):
            self.item = self.tree_goods.identify('item', event.x, event.y)

            if self.item:
                pass
            else:
                try:
                    self.tree_goods.selection_remove(self.tree_goods.selection()[0])
                except IndexError:
                    pass

            update_table(table_goods, self.item)'''

        def bDown(event):
            tv = event.widget

            if tv.identify_row(event.y) not in tv.selection():
                tv.selection_set(tv.identify_row(event.y))

            self.item = tv.identify('item', event.x, event.y)

            if self.item:
                pass
            else:
                try:
                    tv.selection_remove(tv.selection()[0])
                except IndexError:
                    pass

            update_table(table_goods, self.item)

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

        # height = 40
        self.tree_goods = ttk.Treeview(self, height=int(AGO.height_window / 27),
                                       selectmode='browse')

        self.tree_goods.heading('#0', text=_('Categories goods'), anchor='w')

        # minwidth = 350
        self.tree_goods.column("#0", width=350)

        AFT.add_list_goods_tree_from_bd(self.tree_goods)

        self.tree_goods.grid(row=0, column=0, sticky='ew')

        scrollbar_table_goods = Scrollbar(master, orient=HORIZONTAL)

        scrollbar_table_goods["command"] = self.xview
        self["xscrollcommand"] = scrollbar_table_goods.set

        self.create_window((0, 0), window=self.tree_goods, anchor="nw")

        self.tree_goods.bind("<Configure>", rec_canvas)
        # self.tree_goods.bind("<1>", clicks)
        self.tree_goods.bind("<ButtonPress-1>", bDown)
        self.tree_goods.bind("<ButtonRelease-1>", bUp, add='+')
        self.tree_goods.bind("<B1-Motion>", bMove, add='+')

        self.grid(row=2, column=0, columnspan=3, sticky='ew')
        scrollbar_table_goods.grid(row=3, column=0, columnspan=3, sticky='ew')


# Frame for search field, search button and table with goods
class FrameTableGoods(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.config(highlightthickness=0, bd=0)

        self.canvas_table_goods = CanvasTableGoods(master=self)

        self.search_field_button()

        # minsize: 5
        self.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # minsize: 15
        self.columnconfigure(5, {'minsize': int(AGO.width_window / 128)})

        self.grid_columnconfigure(5, weight=1)

        self.grid(row=2, column=2, columnspan=2, sticky='ew')

    # search field, search button and clear button
    def search_field_button(self):
        def search_command():
            row_del = self.canvas_table_goods.table_goods.get_children()

            if row_del:
                goods_id = self.canvas_table_goods.table_goods.item(row_del[0])['values'][0]

                category = SQLite.sel_category_goods_by_id(goods_id)

                for row in row_del:
                    self.canvas_table_goods.table_goods.delete(row)

                rows_ins = SQLite.sel_from_goods_by_product_name(search.get(), category[0][0])
            else:
                rows_ins = SQLite.sel_from_goods_by_product_name(search.get(), '')

            for row in rows_ins:
                # if remains < minimum_balance, then row color - red
                if row[4] < row[7]:
                    self.canvas_table_goods.table_goods.insert('', END,
                                                               values=tuple(row), tags=('red',))
                else:
                    self.canvas_table_goods.table_goods.insert('', END,
                                                               values=tuple(row))

        def search_entry(event):
            search_command()

        # entry search
        entry_search = AGO.CreateEntry(master=self, row=0, column=0, columnspan=3,
                                       key='<Return>', command=search_entry)

        search = entry_search.text

        def clean_search_field():
            entry_search.delete(0, END)

            row_del = self.canvas_table_goods.table_goods.get_children()

            if row_del:
                goods_id = self.canvas_table_goods.table_goods.item(row_del[0])['values'][0]

                category = SQLite.sel_category_goods_by_id(goods_id)

                update_table(self.canvas_table_goods.table_goods, category[0][0])

        for k in range(1, 3):
            self.columnconfigure(k,
                                 {'minsize': int(AGO.width_window / 10.66666666666667)})

        # button search
        AGO.CreateButton(master=self, text=_('Search'), row=0, column=3,
                         command=search_command)

        # button clear
        AGO.CreateButton(master=self, text=_('Clear'), row=0, column=4,
                         command=clean_search_field)


# Canvas for table with goods
class CanvasTableGoods(Canvas):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(highlightthickness=0, bd=0)

        # width = 1350, height = 830
        self.config(height=int(AGO.height_window / 1.301204819277108))

        headings = ('ID', _('Product name'), _('Article'), _('Sale price'),
                    _('Remains'), _('Unit measurement'),
                    _('Up to the minimum remaining balance'),
                    _('Minimum balance'), _('Reserve'))

        # height = 40
        self.table_goods = AGO.CreateTreeview(master=self, height=int(AGO.height_window / 27),
                                              headings=headings, row=0, column=0)

        self.table_goods.tag_configure('red', background='#fc9dad')

        # to highlight a row
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

        def rec_canvas(event):
            self.configure(scrollregion=self.bbox('all'))

        def select(e):
            item = self.table_goods.item(self.table_goods.selection())

            row_id = self.table_goods.identify('item', e.x, e.y)

            if row_id:
                try:
                    WCG.WindowCreateGoods(id_cat=str(item['values'][0]))
                except IndexError:
                    pass
            else:
                pass

        def select_1(e):
            row_id = self.table_goods.identify('item', e.x, e.y)

            if row_id:
                pass
            else:
                try:
                    self.table_goods.selection_remove(self.table_goods.selection()[0])
                except IndexError:
                    pass

        def right_click_menu(e):
            def delete_row():
                category_product = SQLite.sel_category_goods_by_id(str(self.table_goods.set(row_id)['ID']))

                SQLite.del_row_Goods_by_id(str(self.table_goods.set(row_id)['ID']))

                update_table(self.table_goods, category_product[0][0])

            # create a popup menu
            row_id = self.table_goods.identify('item', e.x, e.y)

            if row_id:
                self.table_goods.selection_set(row_id)
                self.table_goods.focus_set()
                self.table_goods.focus(row_id)

                menu = Menu(self, tearoff=0)
                menu.add_command(label=_("Delete"), command=delete_row)
                menu.post(e.x_root, e.y_root)
            else:
                pass

        scrollbar_table_goods = Scrollbar(master, orient=HORIZONTAL)

        scrollbar_table_goods["command"] = self.xview
        self["xscrollcommand"] = scrollbar_table_goods.set

        self.create_window((0, 0), window=self.table_goods, anchor="nw")

        self.table_goods.bind("<Configure>", rec_canvas)
        self.table_goods.bind("<Double-1>", select)
        self.table_goods.bind("<Button-3>", right_click_menu)
        self.table_goods.bind("<1>", select_1)

        self.grid(row=2, column=0, columnspan=100, sticky='ew')
        scrollbar_table_goods.grid(row=3, column=0, columnspan=100, sticky='ew')
