
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
excel = ExcelClass('excel/iranketab_books.xlsx', 'book_list', excel_col_title)
excel.initExcel()

siteUrl = 'https://shahreketabonline.com/Products/Category/216/%D8%B3%DB%8C%D9%86%D9%85%D8%A7'

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

# ? open chrome 
driver.get(siteUrl)

sleep(3)
row = 1


category_links = []

total_page = driver.find_element(By.XPATH, "//*[@id='ProductsTable']/div[2]/div/ul/li[6]/a").text


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

        excel.storeDataInExcel(row, 0, book_name, '0', book_ISBN)
        row += 1

    print('page ' + str(page_num+1) + ' data recieved!')
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((next_page_btn))).click()
    except:
        print('can not get page ' + str(page_num))
        continue

driver.close()
excel.closeExcel()

# ? find cars in brand list
# for option in all_options:
    
#     carBrand = option.find_element(By.CLASS_NAME, "title").text
#     if carName in carBrand:
#         carEnglishName = option.find_element(By.TAG_NAME, "input").get_attribute("value")

#         # ? create excel file and worksheet
#         excel = excel_class('excels/bama_cars_' + carEnglishName + '.xlsx', 'bama_car_list')
#         excel.initExcel()

#         # ? click car checkbox
#         checkbox = option.find_element(By.TAG_NAME, "label")
#         checkbox.click()

#         # ? click submit button to apply filter changes
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'apply'))).click()

#         # ? wait 3 second to apply change
#         sleep(3)

#         total_page = 1
#         while True:
#             print('loading page ' + str(total_page))
#             lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            
#             # ? wait 5 second to get cars by service(http request)
#             sleep(5)


#             lastCount = lenOfPage
#             lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#             # ? check for last page
#             if lastCount == lenOfPage:
#                 break
#             else:
#                 total_page+=1



#         break





# ? request to get book link
def getBookLinks(link):
    try:

        # print('getting course number ' + str(index) + '\n')

        courseResponse = requests.get(link)
        courseHtml = BeautifulSoup(courseResponse.text, 'html.parser')

        # print(courseHtml)
        # ? scrap required data from DOM
        links = courseHtml.find_all(class_='text')

        print(links)
        for link in links:
            print(link)
            excel.storeDataInExcel()


        

        return
    except:
        # print('can`t get course number ' + str(index))
        return


# for x in range(100):
#     print(x)
#     sleep(3 - time() % 1)
#     # getBookLinks('https://www.iranketab.ir/tag/285-dramatic-literature?Page=' + str(x+2))
# getBookLinks('https://shahreketabonline.com/Products/Category/216/%D8%B3%DB%8C%D9%86%D9%85%D8%A7')