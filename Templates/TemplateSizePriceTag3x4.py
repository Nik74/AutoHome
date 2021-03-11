# printing price tag. size 3x4
import os
import time
import SQLite
import datetime

from xhtml2pdf import pisa


def template_price(id_product):
    xhtml = ''

    flag = 0

    date_now = datetime.datetime.now()

    for i in id_product:
        if flag == 1:
            xhtml += '</tr><tr>'

            flag = 0

        product = SQLite.sel_for_price_tag(i)

        xhtml_3_4 = '<td><div class="our_company" align="center">' \
                    'Название вашей компании</div>' \
                    '<div class="inf">' \
                    'Наименование:'  \
                    '<div class="prod_name" align="center">' + product[0][0] + '</div>' \
                    '<br>Ед.:________' + product[0][1] + '' \
                    'Код: ' + str(product[0][2]) + '' \
                    '<div class="mid_font">Цена, руб.:</div>' \
                    '<div class="price" align="center">' + product[0][3] + '</div>' \
                    '<br><div class="small_font">' \
                    'Подпись ответственного лица:' \
                    '<p>___________________________ ' + \
                    date_now.strftime('%d.%m.%Y') + '</p></div>' \
                    '</div></td>'

        xhtml += xhtml_3_4

        if (int(i) % 6) == 0:
            flag = 1

    return xhtml


def printing_io(filename):
    os.startfile(filename, "print")


def template_3x4(id_product):
    filename_pdf = 'printing.pdf'

    xhtml = '<html>' \
            '<head>' \
            '<meta content="text/html"; charset="utf-8"; http-equiv="Content-Type">' \
            '<style type="text/css">' \
            '@font-face {' \
            'font-family: Arial;' \
            'src: url(C:/Windows/Fonts/Arial.ttf);' \
            '}' \
            'table{' \
            'width: 113.814315px;' \
            'height: 151.75242000001px;' \
            'border-collapse: collapse;' \
            'font-size: 30pt;' \
            'font-family: Arial;' \
            'padding: 1px;' \
            '}' \
            'td{' \
            'width: 113.814315px;' \
            '}' \
            'div.our_company{' \
            'width: 113.814315px;' \
            'background: #858585;' \
            'font-size: 34pt;' \
            'height: 22.75px;' \
            'padding: 1px;' \
            '}' \
            'div.inf{' \
            'width: 113.814315px;' \
            'height: 131.00242000001px;' \
            '}' \
            'div.small_font{' \
            'font-size: 19pt;' \
            '}' \
            'div.prod_name{' \
            'font-size: 36pt;' \
            '}' \
            'div.price{' \
            'font-size:56pt;' \
            '}' \
            'div.mid_font{' \
            'font-size:36pt;' \
            '}' \
            '</style>' \
            '</head>' \
            '<body>' \
            '<table border="0.5"><tr>' \

    xhtml += template_price(id_product)

    xhtml += '</tr></table>' \
             '</body>' \
             '</html>'

    pdf = pisa.CreatePDF(xhtml, dest=open(filename_pdf, 'w+b'), encoding='utf-8')

    if not pdf.err:
        pdf.dest.close()

        printing_io(filename_pdf)

        time.sleep(8)
        os.system('taskkill /im AcroRd32.exe /f')
        time.sleep(3)
        os.remove(filename_pdf)
    else:
        print('Unable to create pdf file')
