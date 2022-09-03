
# ! modules:
# ? improt request module for http request
from cmath import log
from webbrowser import Chrome
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

from selenium.webdriver.common.action_chains import ActionChains

import os



# ! classes
# ? import excel class
from classes.excel import ExcelClass




excel_col_title = ['نام کتاب', 'دسته بندی', 'شابک', 'قیمت']

# ? create instance from ecxel class
excel = ExcelClass('excel/iranketab_honar.xlsx', excel_col_title)
# excel.initExcel()

siteUrl = 'https://shahreketabonline.com/'

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

# driver.get(siteUrl)
# sleep(2)
# book_catgory = driver.find_element(By.XPATH, '//*[@id="navbar"]/div[1]')
# # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((book_catgory))).click().perform()

# hover = ActionChains(driver).move_to_element(book_catgory)
# hover.perform()

# sleep(5)

# ? dastan
dastan_category = [
    'https://shahreketabonline.com/Products/Category/199/%D8%AF%D8%A7%D8%B3%D8%AA%D8%A7%D9%86-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86',
    'https://shahreketabonline.com/Products/Category/200/%D8%AF%D8%A7%D8%B3%D8%AA%D8%A7%D9%86-%D8%AC%D9%87%D8%A7%D9%86'
]

# ? adabi
adabi_category = [
    'https://shahreketabonline.com/Products/Category/206/%D9%86%D9%82%D8%AF-%D8%A7%D8%AF%D8%A8%DB%8C',
    'https://shahreketabonline.com/Products/Category/208/%D8%AE%D8%A7%D8%B7%D8%B1%D8%A7%D8%AA-%D9%88-%D8%B3%D9%81%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%88-%D8%B3%D8%B1%DA%AF%D8%B0%D8%B4%D8%AA%D9%86%D8%A7%D9%85%D9%87',
    'https://shahreketabonline.com/Products/Category/207/%D9%85%D8%AA%D9%88%D9%86-%DA%A9%D9%87%D9%86'
]

# ? honar
honar_category = [
    'https://shahreketabonline.com/Products/Category/216/%D8%B3%DB%8C%D9%86%D9%85%D8%A7',
    'https://shahreketabonline.com/Products/Category/217/%D9%86%D9%85%D8%A7%DB%8C%D8%B4',
    'https://shahreketabonline.com/Products/Category/213/%D9%87%D9%86%D8%B1%D9%87%D8%A7%DB%8C-%D8%AA%D8%AC%D8%B3%D9%85%DB%8C',
    'https://shahreketabonline.com/Products/Category/215/%D9%85%D8%B9%D9%85%D8%A7%D8%B1%DB%8C',
    'https://shahreketabonline.com/Products/Category/212/%D9%87%D9%86%D8%B1',
]



def search_in_category(category_url, index):
    driver.get(category_url)

    sleep(3)


    total_page = driver.find_elements(By.CLASS_NAME, "page-item")[5].text
    header = driver.find_elements(By.CLASS_NAME, "header")[0]
    category_title = header.find_elements(By.CLASS_NAME, "title")[0].text
    category_title = category_title.split('کتاب‌های')[1]



    print('starting to crawl category: ' + category_title)

    excel.addSheet(category_title, index)

    # print(category_title)


    print('total page is: ' + total_page)
    
    row = 1
    for page_num in range(int(total_page)):


        while True:
            try:

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

                    book_price = ''

                    try:
                        book_price = book_card.find_elements(By.CLASS_NAME, "price")[0].text
                    except:
                        book_price = 'ناموجود'

                        
                    # print(book_name)
                    # print(book_ISBN)

                    excel.storeDataInExcel(category_title, row, 0, book_name, category_title, book_ISBN, book_price)
                    row = row + 1

                print('page ' + str(page_num+1) + ' data recieved!')
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((next_page_btn))).click()
                except:
                    print('can not get page ' + str(page_num))
                    continue

                break
            except:
                decision = input("error raised while crawling page: " + str(page_num+1) + "\n type y/n for retry ir cancel")
                if decision == 'y':
                    continue

       




index = 0
for catgory in honar_category:
    search_in_category(catgory, index)
    index = index + 1


# search_in_category(siteUrl)


driver.close()
excel.closeExcel()
