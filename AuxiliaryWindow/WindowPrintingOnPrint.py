# Printing a label on a printer

import SQLite

from tkinter import *
from tkinter import ttk, messagebox
from Auxiliary import AuxiliaryGlobalObject as AGO
from Templates import TemplateSizePriceTag35x15 as TSPT35x15, \
    TemplateSizePriceTag3x4 as TSPT3x4, TemplateSizePriceTag60x35 as TSPT60x35,\
    TemplateSizePriceTag60x65 as TSPT60x65

_ = AGO.t.gettext


class WindowPrintingOnPrint(Toplevel):
    def __init__(self, category=None, parent=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Printing a label on a printer"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        self.columnconfigure(0, {'minsize': 5})
        self.columnconfigure(4, {'minsize': 5})

        # label product category
        AGO.CreateLabel(master=self, text=_('Select product category'),
                        row=0, column=1, sticky='w')

        product_category = []

        self.result = ''

        for p_c in SQLite.sel_category_category_goods():
            if p_c != '':
                product_category.append('.'.join(p_c))

        def resize_func(event):
            if type(self.result) == CanvasResultTable:
                self.result.destroy()

                self.result = CanvasResultTable(master=self, category=product_category_comb.get())
            else:
                self.result = CanvasResultTable(master=self, category=product_category_comb.get())

        def printing():
            result_list = []

            if type(self.result) == CanvasResultTable:
                for i in self.result.table_result.selection():
                    item = self.result.table_result.item(i)

                    result_list.append(str(item['values'][0]))

                if result_list:
                    if self.comb_size_price_tag.get() == '3.5x1.5':
                        TSPT35x15.template_35x15(result_list)
                    elif self.comb_size_price_tag.get() == '3x4':
                        TSPT3x4.template_3x4(result_list)
                    elif self.comb_size_price_tag.get() == '6x3.5':
                        TSPT60x35.template_60x35(result_list)
                    elif self.comb_size_price_tag.get() == '6x6.5':
                        TSPT60x65.template_60x65(result_list)
                    else:
                        messagebox.showwarning(_("Warning"),
                                               _('The "Size price tag" field is not completed'),
                                               parent=self)
                else:
                    messagebox.showwarning(_("Warning"),
                                           _('Item has not been selected'),
                                           parent=self)
            else:
                messagebox.showwarning(_("Warning"),
                                       _('Product category not selected'),
                                       parent=self)

        # autocomplete combobox product category
        product_category_comb = AGO.AutocompleteCombobox(master=self, row=0, column=2,
                                                         item=category,
                                                         list_box=product_category,
                                                         command=resize_func,
                                                         events="<<ComboboxSelected>>")

        product_category_comb.configure(width=len(max(product_category)) + 3)

        # button for print price tag
        AGO.CreateButton(master=self, row=0, column=3, text=_('Printing'), command=printing)

        self.rowconfigure(1, {'minsize': 10})

        # label size price tag
        AGO.CreateLabel(master=self, row=2, column=1, text=_('Select size price tag'),
                        sticky='w')

        size_price_tag = ['3.5x1.5', '3x4', '6x3.5', '6x6.5']

        # combobox size price tag
        self.comb_size_price_tag = AGO.CreateCombobox(master=self, list_box=size_price_tag,
                                                      row=2, column=2)

        self.rowconfigure(3, {'minsize': 10})

        if category != '':
            self.result = CanvasResultTable(master=self, category=category)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'),
                                      _('Do you really want to close the window?'),
                                      parent=self):
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)


class CanvasResultTable(Canvas):
    def __init__(self, master=None, category=None):
        super().__init__(master)

        self.master = master
        self.config(highlightthickness=0, bd=0)

        headings = ('ID', _('Product name'))

        rows = SQLite.sel_prod_name_goods_by_category(category)

        def select(e):
            row_id = self.table_result.identify('item', e.x, e.y)

            if row_id:
                pass
            else:
                try:
                    for i in self.table_result.selection():
                        self.table_result.selection_remove(i)
                except IndexError:
                    pass

        self.rowconfigure(1, {'minsize': 5})

        self.table_result = AGO.CreateTreeview(master=self, headings=headings,
                                               rows=rows, row=0, column=0,
                                               selectmode=None)

        self.table_result.bind("<1>", select)

        self.grid_columnconfigure(0, weight=1)

        self.grid(row=4, column=1, columnspan=3, sticky='ew')
