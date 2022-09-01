
# ! modules:
# ? improt request module for http request
from cmath import log
import requests
from requests.exceptions import HTTPError
# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup
# ? import time and speep module
from time import time, sleep

# ? improt selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os



# ! classes
# ? import excel class
from classes.excel import ExcelClass


baseUrl = 'https://www.iranketab.ir/'


excel_col_title = ['نام کتاب', 'دسته بندی', 'شابک']

# ? create instance from ecxel class
excel = ExcelClass('excel/iranketab_books_2.xlsx', 'book_list', excel_col_title)
excel.initExcel()

# siteUrl = 'https://shahreketabonline.com/Products/Category/216/%D8%B3%DB%8C%D9%86%D9%85%D8%A7'

# ? create and return chrome driver
def createChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    # return webdriver.Chrome('/chromedriver/chromedriver 2', options=options)

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "/usr/local/bin/chromedriver")
    # browser = webdriver.Chrome(executable_path = DRIVER_BIN)
    return webdriver.Chrome(executable_path = DRIVER_BIN, options=options)
    

# ? create driver and fix it`s bug
driver = createChromeDriver()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


row = 1


category_links = [
    'https://shahreketabonline.com/Products/Category/196/%D8%AF%D8%A7%D8%B3%D8%AA%D8%A7%D9%86',
    'https://shahreketabonline.com/Products/Category/288/%DA%A9%D9%88%D8%AF%DA%A9-%D9%88-%D9%86%D9%88%D8%AC%D9%88%D8%A7%D9%86',
    'https://shahreketabonline.com/Products/Category/197/%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA',
    'https://shahreketabonline.com/Products/Category/201/%D9%87%D9%86%D8%B1',
    'https://shahreketabonline.com/Products/Category/203/%D8%B1%D9%88%D8%A7%D9%86-%D8%B4%D9%86%D8%A7%D8%B3%DB%8C',
    'https://shahreketabonline.com/Products/Category/204/%D8%B9%D9%84%D9%88%D9%85-%D8%A7%D8%AC%D8%AA%D9%85%D8%A7%D8%B9%DB%8C-%D9%88-%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C',
    'https://shahreketabonline.com/Products/Category/226/%D8%AF%DB%8C%D9%86-%D9%88-%D9%85%D8%B0%D9%87%D8%A8',
    'https://shahreketabonline.com/Products/Category/227/%D9%81%D9%84%D8%B3%D9%81%D9%87-%D9%88-%D8%B9%D8%B1%D9%81%D8%A7%D9%86',
    'https://shahreketabonline.com/Products/Category/228/%D8%AA%D8%A7%D8%B1%DB%8C%D8%AE',
    'https://shahreketabonline.com/Products/Category/288/%DA%A9%D9%88%D8%AF%DA%A9-%D9%88-%D9%86%D9%88%D8%AC%D9%88%D8%A7%D9%86',
]


for catgory in category_links:
    # ? open chrome 
    driver.get(catgory)

    sleep(3)    

    total_page = driver.find_element(By.XPATH, "//*[@id='ProductsTable']/div[2]/div/ul/li[6]/a").text
    header = driver.find_elements(By.CLASS_NAME, "header")[0]
    category_title = header.find_elements(By.CLASS_NAME, "title")[0].text


    print('start crawl category: ' + category_title)
    for page_num in range(int(total_page)):

        # paginator = driver.find_element(By.CLASS_NAME, "pagination")


        sleep(3)
        try:
            next_page_btn = driver.find_element(By.XPATH, "//a[text()='بعدی']")
        except:
            break
        book_card_list = driver.find_elements(By.CLASS_NAME, "ProductWrapper")

        for book_card in book_card_list:
            book_name = book_card.find_elements(By.CLASS_NAME, "text")[0].text
            book_ISBN = ''
            try:
                book_ISBN = (book_card.find_elements(By.CLASS_NAME, "book-image")[0].get_attribute("data-src").split('/')[3]).split('.')[0]
            except:
                book_ISBN = 'نامشخص'
                
            # print(book_name)
            # print(book_ISBN)

            excel.storeDataInExcel(row, 0, book_name, category_title, book_ISBN)
            row += 1

        print('page ' + str(page_num+1) + ' data recieved!')
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((next_page_btn))).click()
        except:
            print('can not get page ' + str(page_num))
            continue



driver.close()
excel.closeExcel()
