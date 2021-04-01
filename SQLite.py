import sqlite3


# function for lower register
from datetime import datetime, date


def lower_string(_str):
    return _str.lower()


conn = sqlite3.connect('SQLiteDB/AutoHome.db')

cursor = conn.cursor()

conn.create_function("lower_s", 1, lower_string)


# Create table for tabs in tree
def create_table_tab():
    cursor.execute("""create table tab
                (id integer not null primary key,
                element text,
                parent text,
                child_index integer)""")

    material = [('Reports', '', 0),
                ('Works by performers', 'Reports', 0),
                ('Ordering outfits on the performers', 'Reports', 1),
                ('Results by artist', 'Reports', 2),
                ('Amounts and debts on documents', 'Reports', 3),
                ('Sales by product', 'Reports', 4),
                ('Repairs by group', 'Reports', 5),
                ('Payments by storage locations', 'Reports', 6),
                ('Profit by month', 'Reports', 7),
                ('Payments', 'Reports', 8),
                ('Shop', '', 0),
                ('Sale of goods', 'Shop', 0),
                ('Provision of the goods', 'Shop', 1),
                ('Product write-off', 'Shop', 2),
                ('Arrival of the goods', 'Shop', 3),
                ('Guides', '', 0),
                ('Works', 'Guides', 0),
                ('Goods', 'Guides', 1),
                ('Brands models', 'Guides', 2),
                ('Staff', 'Guides', 3),
                ('Type of repair', 'Guides', 4),
                ('Categories of payments', 'Guides', 5),
                ('Payment storage locations', 'Guides', 6),
                ('Providers', 'Guides', 7),
                ('Users', 'Guides', 8),
                ('Our company', 'Guides', 9),
                ('Clients', 'Guides', 10),
                ('Car service', '', 0),
                ('Opening a work order', 'Car service', 0),
                ('Closed orders', 'Car service', 1),
                ('Post planner', 'Car service', 2),
                ('Posts', 'Car service', 3)]

    cursor.executemany("""insert into tab 
                        (element, parent, child_index)
                        values (?, ?, ?)""", material)


# Create table for localization of tabs in tree
def create_table_localization_tab():
    cursor.execute("""create table LocalizationTab
                    (id integer not null primary key,
                    table_tab text,
                    id_tab integer,
                    element text,
                    element_ru text)""")

    material = [('tab', 1, 'Reports', 'Отчеты'),
                ('tab', 2, 'Works by performers', 'Работы по исполнителям'),
                ('tab', 3, 'Ordering outfits on the performers', 'Заказ-наряды по исполнителям'),
                ('tab', 4, 'Results by artist', 'Итоги по исполнителям'),
                ('tab', 5, 'Amounts and debts on documents', 'Суммы и долги по документам'),
                ('tab', 6, 'Sales by product', 'Продажи по товарам'),
                ('tab', 7, 'Repairs by group', 'Ремонт по группам'),
                ('tab', 8, 'Payments by storage locations', 'Платежи по местам хранения'),
                ('tab', 9, 'Profit by month', 'Прибыль по месяцам'),
                ('tab', 10, 'Payments', 'Платежи'),
                ('tab', 11, 'Shop', 'Магазин'),
                ('tab', 12, 'Sale of goods', 'Продажи товаров'),
                ('tab', 13, 'Provision of the goods', 'Резерв товаров'),
                ('tab', 14, 'Product write-off', 'Списание товаров'),
                ('tab', 15, 'Arrival of the goods', 'Поступление товаров'),
                ('tab', 16, 'Guides', 'Справочники'),
                ('tab', 17, 'Works', 'Работы'),
                ('tab', 18, 'Goods', 'Товары'),
                ('tab', 19, 'Brands models', 'Марки модели'),
                ('tab', 20, 'Staff', 'Сотрудники'),
                ('tab', 21, 'Type of repair', 'Вид ремонта'),
                ('tab', 22, 'Categories of payments', 'Категории платежей'),
                ('tab', 23, 'Payment storage locations', 'Места хранения платежей'),
                ('tab', 24, 'Providers', 'Поставщики'),
                ('tab', 25, 'Users', 'Пользователи'),
                ('tab', 26, 'Our company', 'Наши компании'),
                ('tab', 27, 'Clients', 'Клиенты'),
                ('tab', 28, 'Car service', 'Автосервис'),
                ('tab', 29, 'Opening a work order', 'Открытие заказ-наряда'),
                ('tab', 30, 'Closed orders', 'Все заказ-наряды'),
                ('tab', 31, 'Post planner', 'Планировщик постов'),
                ('tab', 32, 'Posts', 'Посты')]

    cursor.executemany("""insert into LocalizationTab 
                            (table_tab, id_tab, element, element_ru)
                            values (?, ?, ?, ?)""", material)


# Create table for clients
# inn - ИНН, ogrn - ОГРН, okved - ОКВЭД,
# kpp - КПП, okpo - ОКПО, oktmo - ОКТМО,
# bik - БИК, r_s - Р/С, korr_account - Корр. счет,
def create_table_clients():
    cursor.execute("""create table Clients
                    (id integer not null primary key,
                    client text,
                    type_client text,
                    category text,
                    source text,
                    discount_on_works text, 
                    discount_on_products text,
                    phone_number text(12),
                    another_phone_number text(12),
                    e_mail text,
                    address text,
                    site text,
                    social_networking text,
                    problem_client integer,
                    send_sms integer,
                    send_e_mail integer,
                    inn text,
                    kpp text,
                    ogrn text,
                    okpo text,
                    okved text,
                    oktmo text,
                    bank text,
                    bik text,
                    r_s text,
                    korr_account text,
                    note text)""")


# Create table  for car
# mark - марка машины, license_plate_number - госномер,
# vin - vin, year_release - год выпуска, engine - двигатель,
# gearbox - КПП, body_car - кузов, machine_drive - привод,
# right_hand_drive - правый руль,
# unit_mileage_measurement - единица измерения пробега,
# color - цвет, body_number - номер кузова,
# engine_number - номер двигателя, client - клиент,
# created - создано, model - модель машины
def create_table_car():
    cursor.execute("""create table Car
                    (id integer not null primary key,
                    mark text,
                    model text,
                    license_plate_number text,
                    vin text,
                    year_release text,
                    engine text,
                    gearbox text,
                    body_car text,
                    machine_drive text,
                    right_hand_drive integer,
                    unit_mileage_measurement text,
                    color text,
                    body_number text,
                    engine_number text,
                    client text,
                    created datetime)""")


# Create table for goods
# product_name - название, category - категория,
# article - артикул, unit_measurement - единица измерения,
# quantity_per_pack - количество в упаковке, remains - остаток,
# reserve - резерв, minimum_balance - минимальный остаток,
# up_minimum_remaining_balance - осталось до минимального остатка,
# purchase_price - цена закупки, margin_percentage - процент наценки,
# cost_stock_purchase - стоимость остатков по закупке,
# sale_price - цена продажи, mark_up_amount - сумма наценки,
# cost_sales_balances - стоимость остатков по продаже
# description - описание, image - изображение товара
def create_table_goods():
    cursor.execute("""create table Goods
                    (id integer not null primary key,
                    product_name text,
                    category text,
                    article text,
                    unit_measurement text,
                    quantity_per_pack integer,
                    remains integer,
                    reserve integer,
                    minimum_balance integer,
                    up_minimum_remaining_balance integer,
                    purchase_price text,
                    margin_percentage text,
                    cost_stock_purchase text,
                    sale_price text,
                    mark_up_amount text,
                    cost_sales_balances text,
                    description text,
                    image blob)""")


# Create table for category goods
def create_table_category_goods():
    cursor.execute("""create table Category_goods
                    (id integer not null primary key,
                    element text,
                    parent text,
                    element_number integer)""")


# Create table for payment categories
# category_name - название
def create_table_payment_categories():
    cursor.execute("""create table Payment_categories
                    (id integer not null primary key,
                    category_name text)""")


# Create table for payment storage locations
# payment_storage_locations - место хранения платежей
def create_table_payment_storage_locations():
    cursor.execute("""create table Payment_storage_locations
                    (id integer not null primary key,
                    payment_storage_locations text)""")


# Create table for payments
# payment_amount - сумма платежа, note - примечание,
# payment_category - категория платежа,
# payment_storage_locations - место хранения платежа,
# payment_type - тип платежа, company - компания,
# payment_date - дата платежа
# date_create - дата создания платежа
# move_from - откуда перемещать
# move_to - куда перемещать
def create_table_payments():
    cursor.execute("""create table Payments
                    (id integer not null primary key,
                    payment_amount text,
                    note text,
                    payment_category text,
                    payment_storage_locations text,
                    payment_type text,
                    company text,
                    move_from text,
                    move_to text,
                    payment_date datetime,
                    date_create datetime)""")


# Outputs everything from the tab table
def sel_from_tab():
    cursor.execute("""select tab.*, lt.element_ru
                    from tab, LocalizationTab lt
                    where tab.element = lt.element""")

    return cursor.fetchall()


# Outputs everything from the Clients table
def sel_from_clients():
    cursor.execute("""select cl.id, cl.client, cl.phone_number, 
                        c.license_plate_number, cl.type_client,
                        c.mark_model
                      from Clients cl
                      left join (select client, license_plate_number, (mark || ' ' || model) as mark_model
                                 from Car) c
                        on cl.client = c.client
                      group by cl.id""")

    return cursor.fetchall()


# Outputs from the Clients table by client
def sel_from_clients_by_client(client):
    cursor.execute("""select cl.id, cl.client, cl.phone_number, 
                        c.license_plate_number, cl.type_client,
                        c.mark_model
                      from Clients cl
                      left join (select client, license_plate_number, (mark || ' ' || model) as mark_model
                                 from Car) c
                        on cl.client = c.client
                      where lower_s(cl.client) like lower_s(?)
                      group by cl.id""", (('%{}%'.format(client)),))

    return cursor.fetchall()


# Outputs all from the Clients table
def sel_from_clients_all(id_client):
    cursor.execute("""select *
                    from Clients
                    where id = ?""", (id_client,))

    return cursor.fetchall()


# Outputs client from Clients table
def sel_client_from_clients_by_id(id_client):
    cursor.execute("""select client
                      from Clients
                      where id = ?""", (id_client,))

    return cursor.fetchall()


# Outputs client from Clients table
def sel_client_from_clients():
    cursor.execute("""select client
                    from Clients""")

    return cursor.fetchall()


# Outputs phone_number from Client table
def sel_phone_number_from_client():
    cursor.execute("""select phone_number
                    from Clients""")

    return cursor.fetchall()


# Outputs all from the Car table
def sel_from_car_all(id_car):
    cursor.execute("""select *
                    from Car
                    where id = ?""", (id_car,))

    return cursor.fetchall()


# Output gearbox from Car table
def sel_gearbox_from_car():
    cursor.execute("""select gearbox
                    from Car
                    group by gearbox""")

    return cursor.fetchall()


# Output body_car from Car table
def sel_body_car_from_car():
    cursor.execute("""select body_car
                    from Car
                    group by body_car""")

    return cursor.fetchall()


# Output machine_drive from Car table
def sel_machine_drive_from_car():
    cursor.execute("""select machine_drive
                    from Car
                    group by machine_drive""")

    return cursor.fetchall()


# Output unit_mileage_measurement from Car table
def sel_unit_mileage_measurement_from_car():
    cursor.execute("""select unit_mileage_measurement
                    from Car
                    group by unit_mileage_measurement""")

    return cursor.fetchall()


# Output color from Car table
def sel_color_from_car():
    cursor.execute("""select color
                    from Car
                    group by color""")

    return cursor.fetchall()


# Outputs from Car table
def sel_from_car(client):
    if client:
        cursor.execute("""select c.id, car.mark_model, c.vin, c.client, c.year_release, Ca.name
                          from Car c, (select id, (mark || ' ' ||\
                                       model || ' ' ||\
                                       engine || ' ' ||\
                                       gearbox || ' ' ||\
                                       year_release || ' ' ||\
                                       color || ' ' ||\
                                       license_plate_number) as name
                                       from Car) Ca, (select id, (mark || ' ' || model) as mark_model
                                                      from Car) car
                          where c.id = Ca.id
                          and car.id = c.id
                          and c.client = ?""", (client,))

        return cursor.fetchall()
    else:
        return [('', '', '', '', '', '')]


# Outputs mark from Car table
def sel_mark_from_car():
    cursor.execute("""select mark
                      from Car
                      group by mark""")

    return cursor.fetchall()


# Outputs model from Car table by mark
def sel_model_from_car_by_mark(mark):
    if mark != '':
        cursor.execute("""select model
                          from Car
                          where mark=?
                          group by model""", (mark,))

        return cursor.fetchall()
    else:
        return ''


# Outputs license plate number from Car table
def sel_license_plate_number_from_car():
    cursor.execute("""select license_plate_number
                    from Car""")

    return cursor.fetchall()


# Outputs goods from Goods table by category
def sel_from_goods_by_category(category):
    if category != '':
        cursor.execute("""select id, product_name, article, 
                            sale_price, remains, unit_measurement,
                            up_minimum_remaining_balance,
                            minimum_balance, reserve
                          from Goods
                          where category=?""", (category,))

        return cursor.fetchall()
    else:
        return ''


# Outputs all from Goods table by id
def sel_all_goods_by_id(id_cat):
    cursor.execute("""select *
                    from Goods
                    where id=?""", (id_cat,))

    return cursor.fetchall()


# Outputs category from Goods table by id
def sel_category_goods_by_id(id_element):
    cursor.execute("""select category
                    from Goods
                    where id=?""", (id_element,))

    return cursor.fetchall()


# Outputs article from Goods table
def sel_article_goods():
    cursor.execute("""select article
                    from Goods""")

    return cursor.fetchall()


# Outputs product name from Goods table by category
def sel_prod_name_goods_by_category(category):
    cursor.execute("""select id, product_name
                    from Goods
                    where category=?""", (category,))

    return cursor.fetchall()


# Outputs product name, unit_measurement,
# article, sale_price
def sel_for_price_tag(id_product):
    cursor.execute("""select product_name, unit_measurement,
                             id, sale_price
                    from Goods
                    where id=?""", (id_product,))

    return cursor.fetchall()


# Outputs category from Category_goods table
def sel_category_category_goods():
    cursor.execute("""select element
                    from Category_goods""")

    return cursor.fetchall()


# Outputs all category goods from Category_goods table
def sel_from_category_goods():
    cursor.execute("""select *
                    from Category_goods""")

    return cursor.fetchall()


# Outputs max element number from Category_goods table by parent
def sel_max_number_category_goods(parent):
    cursor.execute("""select max(element_number)
                    from Category_goods
                    where parent=?""", (parent,))

    return cursor.fetchall()


# Outputs element from Category_goods table
def sel_element_category_goods():
    cursor.execute("""select element
                    from Category_goods""")

    return cursor.fetchall()


# outputs element from Category_goods where parent = ''
def sel_element_category_goods_by_parent():
    cursor.execute("""select element
                    from Category_goods
                    where parent=''""")

    return cursor.fetchall()


# outputs all from Category_goods where parent = ''
def sel_all_category_goods_by_parent():
    cursor.execute("""select *
                    from Category_goods
                    where parent=''""")

    return cursor.fetchall()


# outputs all from Category_goods where parent != ''
def sel_all_category_goods_by_parent_2():
    cursor.execute("""select *
                    from Category_goods
                    where parent<>''""")

    return cursor.fetchall()


# Outputs goods from Goods table by product name
def sel_from_goods_by_product_name(product, category):
    if product != '':
        if category == '':
            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                            from Goods
                            where lower_s(product_name) like lower_s(?)""", (('%{}%'.format(product)),))

            result = cursor.fetchall()

            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                            from Goods
                            where id = ?""", (product,))

            for k in cursor.fetchall():
                if k not in result:
                    result.append(k)

            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                            from Goods
                            where article = ?""", (product,))

            for k in cursor.fetchall():
                if k not in result:
                    result.append(k)

            return result
        else:
            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                               from Goods
                               where lower_s(product_name) like lower_s(?)
                               and category=?""",
                           (('%{}%'.format(product)), category))

            result = cursor.fetchall()

            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                            from Goods
                            where id = ?
                            and category=?""", (product, category))

            for k in cursor.fetchall():
                if k not in result:
                    result.append(k)

            cursor.execute("""select id, product_name, article, 
                                sale_price, remains, unit_measurement,
                                up_minimum_remaining_balance,
                                minimum_balance, reserve
                            from Goods
                            where article = ?
                            and category=?""", (product, category))

            for k in cursor.fetchall():
                if k not in result:
                    result.append(k)

            return result
    else:
        return ''


# select all from Payment_categories table
def sel_from_payment_categories():
    cursor.execute("""select *
                    from Payment_categories""")

    return cursor.fetchall()


# select category_name from Payment_categories table
def sel_category_name_from_payment_categories():
    cursor.execute("""select category_name
                    from Payment_categories""")

    return cursor.fetchall()


# select payment storage locations from Payment_storage_locations table
def sel_payment_storage_locations_from_payment_storage_locations():
    cursor.execute("""select payment_storage_locations
                    from Payment_storage_locations""")

    return cursor.fetchall()


# select all from Payment_storage_locations
def sel_from_payment_storage_locations():
    cursor.execute("""select *
                    from Payment_storage_locations""")

    return cursor.fetchall()


# change after create order!!!!
# select all from Payments table by payment_date
def sel_from_payments_by_payment_date(date_from, date_to):
    if type(date_from) == str:
        date_from = datetime.strptime(date_from, '%d.%m.%Y')
        date_to = datetime.strptime(date_to, '%d.%m.%Y')

    date_from = date_from.strftime('%Y-%m-%d')

    date_to = date_to.strftime('%Y-%m-%d')

    cursor.execute("""select id, payment_date, payment_type,
                        payment_storage_locations,
                        payment_category, payment_amount,
                        move_from, move_to, null, null, 
                        date_create, null, null, company
                    from Payments
                    where payment_date between ? and ?""", (date_from, date_to))

    return cursor.fetchall()


# select from Payments table by id
def sel_from_payments_by_id(id_payments):
    cursor.execute("""select payment_amount, note,
                        payment_category, payment_storage_locations,
                        payment_type, company, payment_date, date_create
                    from Payments
                    where id=?""", (id_payments,))

    return cursor.fetchall()


# select from Payments table by id
def sel_from_payments_by_id_for_transfer(id_transfer):
    cursor.execute("""select payment_amount, move_from, move_to, 
                        note, payment_type, company, 
                        payment_date, date_create
                    from Payments
                    where id=?""", (id_transfer,))

    return cursor.fetchall()


# select sum(payment_amount) from Payments table
def sel_sum_payment_amount_from_payments():
    cursor.execute("""select sum(payment_amount)
                    from Payments""")

    return cursor.fetchall()


# select max(payment_date) from Payments table
def sel_max_payment_date_from_Payments():
    cursor.execute("""select max(payment_date)
                    from Payments""")

    return cursor.fetchall()


# select min(payment_date) from Payments table
def sel_min_payment_date_from_Payments():
    cursor.execute("""select min(payment_date)
                    from Payments""")

    return cursor.fetchall()


# select payment_amount and payment_category from Payments table by id
def sel_amount_category_from_payments_by_id(id_payments):
    cursor.execute("""select payment_amount, payment_category
                    from Payments
                    where id=?""", (id_payments,))

    return cursor.fetchall()


# change after create order!!!!
# select for print PKO from Payments table
def sel_for_PKO_from_payments_by_id(id_payment):
    cursor.execute("""select payment_date, id, payment_amount,
                        null, payment_category
                    from Payments
                    where id=?""", (id_payment,))

    return cursor.fetchall()


# insert in table Clients
def ins_Client(client):
    cursor.execute("""insert into Clients(client, type_client, category, source, discount_on_works, 
                                        discount_on_products, phone_number, another_phone_number, 
                                        e_mail, address, site, social_networking, problem_client, 
                                        send_sms, send_e_mail, inn, kpp, ogrn, okpo, okved, oktmo, bank, bik, r_s, 
                                        korr_account, note)
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?)""", client)
    conn.commit()


# insert in table Clients
def ins_Car(car):
    cursor.execute("""insert into Car(mark, model, license_plate_number, vin, year_release, engine,
                                      gearbox, body_car, machine_drive, right_hand_drive, 
                                      unit_mileage_measurement, color, body_number, engine_number,
                                      client, created)
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", car)
    conn.commit()


# insert in table Category_goods
def ins_Category_goods(category_goods):
    cursor.execute("""insert into Category_goods(element, parent, element_number)
                    values (?, ?, ?)""", category_goods)

    conn.commit()


# insert in table Goods
def ins_Goods(product):
    cursor.execute("""insert into Goods(product_name, category,
                        article, unit_measurement,
                        quantity_per_pack, remains,
                        reserve, minimum_balance,
                        up_minimum_remaining_balance,
                        purchase_price, margin_percentage,
                        cost_stock_purchase, sale_price,
                        mark_up_amount, cost_sales_balances,
                        description, image)
                       values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", product)
    conn.commit()


# insert in Payment_categories table
def ins_Payment_categories(category_name):
    cursor.execute("""insert into Payment_categories(category_name)
                    values (?)""", (category_name,))

    conn.commit()


# insert in Payment_storage_locations table
def ins_Payment_storage_locations(payment_storage_locations):
    cursor.execute("""insert into Payment_storage_locations(payment_storage_locations)
                    values(?)""", (payment_storage_locations,))

    conn.commit()


# insert in Payments table
def ins_Payments(payment):
    cursor.execute("""insert into Payments(payment_amount,
                        note, payment_category,
                        payment_storage_locations,
                        payment_type, company,
                        payment_date,
                        date_create)
                    values(?,?,?,?,?,?,?,?)""", payment)

    conn.commit()


# insert in Payments table
def ins_Payments_for_transfer(transfer):
    cursor.execute("""insert into Payments(payment_category,
                        payment_amount,
                        move_from, move_to,
                        note, payment_type,
                        company, payment_date,
                        date_create,
                        payment_storage_locations)
                    values(?,?,?,?,?,?,?,?,?,?)""", transfer)

    conn.commit()


# update row in Clients table
def upd_Clients(client):
    cursor.execute("""update Clients
                        set client=?, type_client=?, category=?, source=?, discount_on_works=?, 
                            discount_on_products=?, phone_number=?, another_phone_number=?, 
                            e_mail=?, address=?, site=?, social_networking=?, problem_client=?, 
                            send_sms=?, send_e_mail=?, inn=?, kpp=?, ogrn=?, okpo=?, okved=?, oktmo=?,
                            bank=?, bik=?, r_s=?, korr_account=?, note=?
                        where id=?""", client)
    conn.commit()


# update row in Client table by phone_number
def upd_Client_by_phone_number(phone_number):
    cursor.execute("""update Clients
                        set client=?, type_client=?, category=?, source=?, discount_on_works=?, 
                            discount_on_products=?, phone_number=?, another_phone_number=?, 
                            e_mail=?, address=?, site=?, social_networking=?, problem_client=?, 
                            send_sms=?, send_e_mail=?, inn=?, kpp=?, ogrn=?, okpo=?, okved=?, oktmo=?,
                            bank=?, bik=?, r_s=?, korr_account=?, note=?
                    where phone_number=?""", phone_number)

    conn.commit()


# update row in Car table
def upd_Car(car):
    cursor.execute("""update Car
                        set mark=?, model=?, license_plate_number=?, vin=?, year_release=?, engine=?,
                            gearbox=?, body_car=?, machine_drive=?, right_hand_drive=?, 
                            unit_mileage_measurement=?, color=?, body_number=?, engine_number=?,
                            client=?, created=?
                        where id=?""", car)
    conn.commit()


# update row in Car table by license plate number
def upd_Car_by_license_plate_number(car):
    cursor.execute("""update Car
                        set mark=?, model=?, license_plate_number=?, vin=?, year_release=?, engine=?,
                            gearbox=?, body_car=?, machine_drive=?, right_hand_drive=?, 
                            unit_mileage_measurement=?, color=?, body_number=?, engine_number=?,
                            client=?, created=?
                        where license_plate_number=?""", car)
    conn.commit()


# update client in Car table by client
def upd_Car_by_client(new_client, old_client):
    cursor.execute("""update Car
                        set client=?
                    where client=?""", (new_client, old_client))

    conn.commit()


# update element in Category_goods table
def upd_Category_goods_by_element(new_element, element):
    cursor.execute("""update Category_goods
                        set parent=?
                        where parent=?""", (new_element, element))

    cursor.execute("""update Goods
                    set category=?
                    where category=?""", (new_element, element))

    cursor.execute("""update Category_goods
                    set element=?
                    where element=?""", (new_element, element))

    conn.commit()


# update row in Goods table
def upd_Goods(product):
    cursor.execute("""update Goods
                        set product_name=?, category=?,
                        article=?, unit_measurement=?,
                        quantity_per_pack=?, remains=?,
                        reserve=?, minimum_balance=?,
                        up_minimum_remaining_balance=?,
                        purchase_price=?, margin_percentage=?,
                        cost_stock_purchase=?, sale_price=?,
                        mark_up_amount=?, cost_sales_balances=?,
                        description=?, image=?
                      where id=?""", product)

    conn.commit()


# update row in Goods table by article
def upd_Goods_by_article(product):
    cursor.execute("""update Goods
                        set product_name=?, category=?,
                        article=?, unit_measurement=?,
                        quantity_per_pack=?, remains=?,
                        reserve=?, minimum_balance=?,
                        up_minimum_remaining_balance=?,
                        purchase_price=?, margin_percentage=?,
                        cost_stock_purchase=?, sale_price=?,
                        mark_up_amount=?, cost_sales_balances=?,
                        description=?, image=?
                      where article=?""", product)

    conn.commit()


# update row in Payments table by id
def upd_payments_by_id(inf_payments):
    cursor.execute("""update Payments
                        set payment_amount=?,
                        note=?,
                        payment_category=?,
                        payment_storage_locations=?,
                        payment_type=?,
                        company=?,
                        payment_date=?,
                        date_create=?
                    where id=?""", inf_payments)

    conn.commit()


# update row in payments table by id for transfer funds
def upd_payments_by_id_for_transfer(inf_transfer):
    cursor.execute("""update Payments
                        set payment_category=?,
                        payment_amount=?,
                        move_from=?,
                        move_to=?,
                        note=?,
                        payment_type=?,
                        company=?,
                        payment_date=?,
                        date_create=?,
                        payment_storage_locations
                    where id=?""", inf_transfer)

    conn.commit()


# swapping the rows in Category_goods table
def swap_rows_Category_goods(element_1, element_2):
    cursor.execute("""update Category_goods
                    set element=(case when element=? then ? else ? end)
                    where element in (?,?)""", (element_1, element_2,
                                                element_1, element_1,
                                                element_2))

    conn.commit()


# delete row in Clients table
def del_row_Clients(id_client):
    cursor.execute("""delete from Clients
                        where id=?""", (id_client,))
    conn.commit()


# delete row in Car table
def del_row_Car_by_id(id_client):
    cursor.execute("""delete from Car
                      where id=?""", (id_client,))
    conn.commit()


# delete row in Car table
def del_row_Car_by_client(client):
    cursor.execute("""delete from Car
                      where client=?""", (client,))
    conn.commit()


# delete rows in Category_goods table by parent
def del_rows_Category_goods_by_parent(parent):
    cursor.execute("""select element
                        from Category_goods
                        where parent=?""", parent)

    for i in cursor.fetchall():
        del_rows_Category_goods_by_parent(i)

    cursor.execute("""delete from Goods
                        where category=?""", parent)

    cursor.execute("""delete from Category_goods
                      where element=?""", parent)

    conn.commit()


# delete row in Goods table
def del_row_Goods_by_id(id_product):
    cursor.execute("""delete from Goods
                    where id=?""", (id_product,))

    conn.commit()


# delete row in Payment_categories by id
def del_row_Payment_categories_by_id(id_category):
    cursor.execute("""delete from Payment_categories
                    where id=?""", (id_category,))

    conn.commit()


# delete row in Payment_storage_locations by id
def del_row_Payment_storage_locations_by_id(id_payment_storage_locations):
    cursor.execute("""delete from Payment_storage_locations
                    where id=?""", (id_payment_storage_locations,))

    conn.commit()


# delete row in Payments table by id
def del_row_Payments_by_id(id_payments):
    cursor.execute("""delete from Payments
                    where id=?""", (id_payments,))

    conn.commit()


# alter column in Goods table
def alt_col_Goods():
    cursor.execute("""alter table Goods add column image blob""")

    conn.commit()


############################################################################################################
# Insert
def ins():
    cursor.execute("""insert into Clients (client, phone_number, number_car, type_client, mark_car)
                    values('Герасимов Никита', '89517837392', 'Х788ВВ96', 'Физлицо', 'Honda Civic 5d 2008')""")


# Update
def upd():
    cursor.execute("""update tab
                    set element='Clients'
                    where element='Client'""")


def del_table():
    cursor.execute("""drop table Payments""")


# Select
def sel():
    cursor.execute("""select *
                    from Payments""")

    return cursor.fetchall()

#print(sel())

#conn.commit()
