
# ! class

from classes.book import BookClass
from classes.excel import ExcelClass

# ! modules:

# ? import thrading module
import threading
# ? improt request module for http request
import requests
from requests.exceptions import HTTPError
# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup
# ? import time and speep module
from time import time, sleep


baseUrl = "https://www.30book.com/book/"
total_book = 137360


excel_col_title = ['نام کتاب', 'دسته بندی', 'قیمت', 'ویژگی']

# ? create instance from ecxel class
excel = ExcelClass('excel/30_book.xlsx', excel_col_title)
excel.addSheet('book', 0)

row = 1
for book_index in range(100):
    print('getting index '+ str(book_index+1))

    try:

        book_detail_html = requests.get(baseUrl + str(book_index+1))
        beauty_html = BeautifulSoup(book_detail_html.text, 'html.parser')


        book_title = beauty_html.find(class_='ProductTitle').get_text()
        attrs = beauty_html.find_all(class_='Attribute')
        price = beauty_html.find(class_='Price').get_text()
        unavailable = beauty_html.find(class_='unavailable-text')


        category = ''

        try:
            category = beauty_html.find(class_='col-sm-4').find(class_='blue').get_text().strip()
        except:
            category = 'نامشخص'

        if (unavailable):
            price += '(ناموجود)'



        # print(book_title)

        attr_string = ''
        for attr in attrs:
            # print((attr.find(class_="col-3").get_text()).strip())
            # print((attr.find(class_="col-9").get_text()).strip())

            attr_string += (attr.find(class_="col-3").get_text()).strip() + (attr.find(class_="col-9").get_text()).strip() + ' | '

        excel.storeDataInExcel('book', row, 0, book_title, category, price, attr_string)
        row += 1

    except:
        print('can not get index ' + str(book_index+1))
        continue


excel.closeExcel()



    