# here a window is created for adding a product
import os
import PIL
import SQLite

from PIL import ImageTk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from Auxiliary import AuxiliaryGlobalObject as AGO, \
    AuxiliaryFunctions as AF

_ = AGO.t.gettext


# rounding to 0 or 5
def my_round(x, base=5):
    return base * round(x / base)


class WindowCreateGoods(Toplevel):
    def __init__(self, category='', id_cat=None, parent=None):
        super().__init__(parent)

        self.grab_set()

        self.title(_("Create product"))
        self.iconbitmap(AGO.path_logo_ico)

        style = ttk.Style()
        style.theme_use('vista')

        # minsize: 5
        self.columnconfigure(0, {'minsize': int(AGO.width_window / 384)})
        self.columnconfigure(2, {'minsize': int(AGO.width_window / 384)})

        # minsize: 5
        self.rowconfigure(0, {'minsize': int(AGO.height_window / 216)})
        self.rowconfigure(4, {'minsize': int(AGO.height_window / 216)})

        # minsize: 10
        self.rowconfigure(2, {'minsize': int(AGO.height_window / 108)})

        self.product = FrameInformationProduct(master=self, category=category, id_cat=id_cat).product

        FrameButtons(master=self, product=self.product, id_cat=id_cat)

        # messagebox: Question when closing the window
        def on_close():
            if messagebox.askokcancel(_('Exit'), _('Do you really want to close the window?'),
                                      parent=self):

                for file in os.listdir("./"):
                    if file.endswith(".gif"):
                        os.remove(file)

                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)


# Frame for buttons save and exit, and save
class FrameButtons(Frame):
    def __init__(self, master=None, product=None, id_cat=None):
        super().__init__(master)

        self.master = master

        def save_product():
            inf_product = list()

            check_article = SQLite.sel_article_goods()
            check_category = SQLite.sel_category_category_goods()

            if (product.get('category').get(),) not in check_category:
                messagebox.showwarning(_("Warning"),
                                       _('There is no such category'),
                                       parent=master)
                return 0

            if product.get('product_name').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "product name" field is not completed'),
                                       parent=master)
                return 0

            if product.get('category').get() == '':
                messagebox.showwarning(_("Warning"),
                                       _('The "category" field is not completed'),
                                       parent=master)
                return 0

            if product.get('article').get() == '':
                messagebox.showwarning(_('Warning'),
                                       _('The "article" field is not completed'),
                                       parent=master)
                return 0

            for i in product.values():
                if type(i) is AGO.CreateText:
                    if i.get(1.0, END) != '\n':
                        inf_product.append(i.get(1.0, END))
                    else:
                        inf_product.append('')
                elif type(i) is str:
                    inf_product.append(i)
                elif type(i) is bytes:
                    inf_product.append(i)
                else:
                    inf_product.append(i.get())

            if id_cat is not None:
                inf_product.append(id_cat)

                SQLite.upd_Goods(inf_product)
            else:
                if (product.get('article').get(),) in check_article:
                    inf_product.append(product.get('article').get())

                    SQLite.upd_Goods_by_article(inf_product)
                else:
                    SQLite.ins_Goods(inf_product)

        # Save and exit
        def save_product_and_exit():
            err = save_product()

            if err is None:
                for file in os.listdir("./"):
                    if file.endswith(".gif"):
                        os.remove(file)

                master.destroy()

        AGO.CreateButton(master=self, text=_('Save and exit'), row=0,
                         column=0, command=save_product_and_exit)

        AGO.CreateButton(master=self, text=_('Save'), row=0,
                         column=1, command=save_product)

        self.grid(row=1, column=1, sticky='ew')


def view_img(frame, item, path=None, prod_name='img'):
    if path is None:
        if prod_name is not None:
            path_img = prod_name + '.gif'

            AF.write_file(item, path_img)
    else:
        path_img = path

    if os.path.exists(path_img):
        img = PIL.Image.open(path_img)
        img = img.resize((100, 100), PIL.Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel_img = AGO.CreateLabel(master=frame, row=3, column=1, sticky='w')
        panel_img.config(image=img)
        panel_img.image = img
    else:
        messagebox.showerror(_('Error'),
                             _('Image ') + path_img + _(' not found!'),
                             parent=frame)


# Frame to fill in the information about the product
class FrameInformationProduct(Frame):
    def __init__(self, master=None, category='', id_cat=None):
        super().__init__(master)

        self.master = master

        self.product = dict()

        self.grid_columnconfigure(1, weight=1)

        self.grid_columnconfigure(3, weight=1)

        item = ['' for x in range(0, 18)]

        if id_cat is not None:
            sel_product = SQLite.sel_all_goods_by_id(id_cat)

            if sel_product is not None:
                item = list(sel_product[0])

        # label product name
        AGO.CreateLabel(master=self, text=_('Product name'), row=0,
                        column=0, anchor='w')

        # entry product name
        self.product['product_name'] = AGO.CreateEntry(master=self, row=0, column=1,
                                                       columnspan=3, item=item[1]).text
        # label category
        AGO.CreateLabel(master=self, text=_('Category'), row=1, column=0, anchor='w')

        category_product = []

        for cp in SQLite.sel_element_category_goods():
            if cp != ('',):
                category_product.append('.'.join(cp))

        if item[2] == '':
            item[2] = category

        # entry category
        self.product['category'] = AGO.AutocompleteCombobox(master=self, row=1, column=1,
                                                            columnspan=3, item=item[2],
                                                            list_box=category_product)
        # label article
        AGO.CreateLabel(master=self, text=_('Article'), row=2, column=0, anchor='w')

        # entry article
        self.product['article'] = AGO.CreateEntry(master=self, row=2, column=1,
                                                  columnspan=3, item=item[3]).text
        # label unit measurement
        AGO.CreateLabel(master=self, text=_('Unit measurement'), row=3,
                        column=0, anchor='w')

        # entry unit measurement
        self.product['unit_measurement'] = AGO.CreateEntry(master=self, row=3, column=1,
                                                           item=item[4]).text
        # label quantity per pack
        AGO.CreateLabel(master=self, text=_('Quantity per pack'), row=3,
                        column=2, anchor='w')

        # entry quantity per pack
        self.product['quantity_per_pack'] = AGO.CreateEntry(master=self, row=3, column=3,
                                                            item=item[5]).text

        # minsize: 5
        self.rowconfigure(4, {'minsize': int(AGO.height_window / 216)})

        # frame for remains
        frame_remains = Frame(self, highlightbackground="black",
                              highlightcolor='black', highlightthickness=1, bd=0)

        # big label remains
        AGO.CreateLabel(master=frame_remains, text=_('Remains'), bg='#cac7c6', anchor='w',
                        row=0, column=0, columnspan=10)

        # minsize: 5
        frame_remains.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # minsize: 10
        frame_remains.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})
        frame_remains.columnconfigure(9, {'minsize': int(AGO.width_window / 192)})

        # label remains
        AGO.CreateLabel(master=frame_remains, text=_('Remains'), row=2, column=1)

        if item[6] == '':
            item[6] = '0'

        def upd_up_min_rem_bal(e):
            try:
                item[9] = int(self.product['remains'].get()) - int(self.product['minimum_balance'].get())
            except ValueError:
                pass

            # entry up minimum remaining balance
            self.product['up_minimum_remaining_balance'] = AGO.CreateEntry(master=frame_remains,
                                                                           row=2, column=8,
                                                                           item=item[9]).text

        # entry remains
        self.product['remains'] = AGO.CreateEntry(master=frame_remains, row=2, column=2,
                                                  item=item[6], key='<Return>',
                                                  command=upd_up_min_rem_bal).text
        # label reserve
        AGO.CreateLabel(master=frame_remains, text=_('Reserve'), row=2, column=3)

        # entry reserve
        self.product['reserve'] = AGO.CreateEntry(master=frame_remains, row=2, column=4,
                                                  item=item[7]).text
        # label minimum balance
        AGO.CreateLabel(master=frame_remains, text=_('Minimum balance'),
                        row=2, column=5)

        if item[8] == '':
            item[8] = 0

        self.product['minimum_balance'] = AGO.CreateEntry(master=frame_remains, row=2,
                                                          column=6, item=item[8],
                                                          key='<Return>',
                                                          command=upd_up_min_rem_bal).text
        # label up minimum remaining balance
        AGO.CreateLabel(master=frame_remains, text=_('Up minimum remaining balance'),
                        row=2, column=7)

        if item[9] == '':
            item[9] = int(item[6]) - int(item[8])

        # entry up minimum remaining balance
        self.product['up_minimum_remaining_balance'] = AGO.CreateEntry(master=frame_remains,
                                                                       row=2, column=8,
                                                                       item=item[9]).text

        frame_remains.rowconfigure(3, {'minsize': 5})

        frame_remains.grid(row=5, column=0, columnspan=4, sticky='ew')

        # minsize: 10
        self.rowconfigure(6, {'minsize': int(AGO.height_window / 108)})

        # frame for cost
        frame_cost = Frame(self, highlightbackground="black",
                           highlightcolor='black', highlightthickness=1, bd=0)

        # label cost
        AGO.CreateLabel(master=frame_cost, text=_('Cost'), bg='#cac7c6', anchor='w',
                        row=0, column=0, columnspan=8)

        # minsize: 5
        frame_cost.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # minsize: 10
        frame_cost.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})
        frame_cost.columnconfigure(7, {'minsize': int(AGO.width_window / 192)})

        frame_cost.grid_columnconfigure(2, weight=1)
        frame_cost.grid_columnconfigure(4, weight=1)
        frame_cost.grid_columnconfigure(6, weight=1)

        # label purchase price
        AGO.CreateLabel(master=frame_cost, text=_('Purchase price'), row=2,
                        column=1, sticky='w')

        def upd_mark_up_amount(e):
            item[14] = round(int(self.product['sale_price'].get()) - \
                             float(self.product['purchase_price'].get()), 2)

            self.product['mark_up_amount'] = AGO.CreateEntry(master=frame_cost, row=4,
                                                             column=4, item=item[14]).text

        if item[10] == '':
            item[10] = 0

        # entry purchase price
        self.product['purchase_price'] = AGO.CreateEntry(master=frame_cost, row=2,
                                                         column=2, item=item[10],
                                                         key='<Return>',
                                                         command=upd_mark_up_amount).text
        # label margin percentage
        AGO.CreateLabel(master=frame_cost, row=2, column=3, text=_('Margin percentage'),
                        sticky='w')

        def upd_sale_price(e):
            item[13] = my_round(float(self.product['purchase_price'].get()) + \
                                float(self.product['purchase_price'].get()) / 100 * \
                                int(self.product['margin_percentage'].get()))

            self.product['sale_price'] = AGO.CreateEntry(master=frame_cost, row=4,
                                                         column=2, item=item[13],
                                                         key='<Return>',
                                                         command=upd_mark_up_amount).text

            upd_mark_up_amount(e)

        if item[11] == '':
            item[11] = 0

        # entry margin percentage
        self.product['margin_percentage'] = AGO.CreateEntry(master=frame_cost, row=2,
                                                            column=4, item=item[11],
                                                            key='<Return>',
                                                            command=upd_sale_price).text
        # label cost stock purchase
        AGO.CreateLabel(master=frame_cost, row=2, column=5, text=_('Cost stock purchase'),
                        sticky='w')

        # entry cost stock purchase
        self.product['cost_stock_purchase'] = AGO.CreateEntry(master=frame_cost, row=2,
                                                              column=6, item=item[12]).text

        # minsize: 5
        frame_cost.rowconfigure(3, {'minsize': int(AGO.height_window / 216)})

        # label sale price
        AGO.CreateLabel(master=frame_cost, text=_('Sale price'), row=4, column=1,
                        sticky='w')

        if item[13] == '':
            item[13] = 0

        # entry sale_price
        self.product['sale_price'] = AGO.CreateEntry(master=frame_cost, row=4,
                                                     column=2, item=item[13],
                                                     key='<Return>',
                                                     command=upd_mark_up_amount).text
        # label mark up amount
        AGO.CreateLabel(master=frame_cost, text=_('Mark up amount'), row=4, column=3,
                        sticky='w')

        if item[14] == '':
            item[14] = round(int(item[13]) - float(item[10]), 2)

        # entry mark up amount
        self.product['mark_up_amount'] = AGO.CreateEntry(master=frame_cost, row=4,
                                                         column=4, item=item[14]).text
        # label cost sales balances
        AGO.CreateLabel(master=frame_cost, text=_('Cost sales balances'), row=4, column=5,
                        sticky='w')

        # entry cost sales balances
        self.product['cost_sales_balances'] = AGO.CreateEntry(master=frame_cost, row=4,
                                                              column=6, item=item[15]).text

        # minsize: 5
        frame_cost.rowconfigure(7, {'minsize': int(AGO.height_window / 216)})

        frame_cost.grid(row=7, column=0, columnspan=4, sticky='ew')

        # minsize: 10
        self.rowconfigure(8, {'minsize': int(AGO.height_window / 108)})

        # minsize: 10
        self.rowconfigure(10, {'minsize': int(AGO.height_window / 108)})

        # label description
        AGO.CreateLabel(master=self, text=_('Description'), row=11, column=0, sticky='w')

        # text description
        self.product['note'] = AGO.CreateText(master=self, height=int(AGO.height_window / 108),
                                              item=item[16], row=12, column=0, columnspan=4, sticky='ew')

        # frame for image
        frame_img = Frame(self, highlightbackground="black",
                          highlightcolor='black', highlightthickness=1, bd=0)

        # label cost
        AGO.CreateLabel(master=frame_img, text=_('Image'), bg='#cac7c6', anchor='w',
                        row=0, column=0, columnspan=4)

        # minsize: 5
        frame_img.rowconfigure(1, {'minsize': int(AGO.height_window / 216)})

        # minsize: 10
        frame_img.columnconfigure(0, {'minsize': int(AGO.width_window / 192)})

        def browse_func():
            filename = filedialog.askopenfilename(parent=self)
            label_img.config(text=filename)

            view_img(frame_img, filename, path=filename)

            if filename:
                with open(filename, 'rb') as file:
                    self.product['path_img'] = file.read()

        # browse button
        browse_button = AGO.CreateButton(master=frame_img, text=_('Browse'),
                                         command=browse_func)

        browse_button.grid(row=2, column=2)

        # label for view image path
        label_img = AGO.CreateLabel(master=frame_img, row=2,
                                    column=1, sticky='w')

        label_img.config(text='')

        self.product['path_img'] = ''

        if item[17] != '' and item[17] is not None:
            view_img(frame_img, item[17])

            self.product['path_img'] = item[17]

        # minsize: 10
        frame_img.columnconfigure(3, {'minsize': int(AGO.width_window / 192)})

        frame_img.grid_columnconfigure(3, weight=1)

        # minsize: 5
        frame_img.rowconfigure(4, {'minsize': int(AGO.height_window / 216)})

        frame_img.grid(row=9, column=0, columnspan=4, sticky='ew')

        self.grid(row=3, column=1, sticky='ew')
