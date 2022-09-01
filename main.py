
# ! modules:
# ? improt request module for http request
import requests
from requests.exceptions import HTTPError
# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup



# ! classes
# ? import excel class
from classes.excel import ExcelClass





excel_col_title = ['نام کتاب', 'دسته بندی', 'شابک']

# ? create instance from ecxel class
excel = ExcelClass('excel/iranketab_books.xlsx', 'book_list', excel_col_title)

