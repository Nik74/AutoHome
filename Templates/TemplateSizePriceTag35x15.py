# printing price tag. size 3.5x1.5
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

        xhtml_35_15 = '<td><div class="our_company" align="center">' \
                      'Название вашей компании</div>' \
                      '<div class="inf">' \
                      '<div class="prod_name" align="center">' + product[0][0] + '</div>' \
                      '<br>Ед.:________' + product[0][1] + '' \
                      'Код: ' + str(product[0][2]) + '' \
                      '<br>Цена, руб.: ' + product[0][3] + '' \
                      '<br><div class="small_font">' \
                      'Подпись: _________________________________________ ' + \
                      date_now.strftime('%d.%m.%Y') + '</div>' \
                      '</div></td>'

        xhtml += xhtml_35_15

        if (int(i) % 5) == 0:
            flag = 1

    return xhtml


def printing_io(filename):
    os.startfile(filename, "print")


def template_35x15(id_product):
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
            'width: 132.7833675px;' \
            'height: 56.9071575px;' \
            'border-collapse: collapse;' \
            'font-size: 8pt;' \
            'font-family: Arial;' \
            'padding: 1px;' \
            '}' \
            'td{' \
            'width: 132.7833675px;' \
            '}' \
            'div.our_company{' \
            'width: 132.7833675px;' \
            'font-size: 10pt;' \
            'background: #858585;' \
            'height: 16px;' \
            '}' \
            'div.inf{' \
            'width: 132.7833675px;' \
            'height: 42.9071575px;' \
            '}' \
            'div.small_font{' \
            'font-size: 7pt;' \
            '}' \
            'div.prod_name{' \
            'font-size: 18pt;' \
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
