
# ! class

# from asyncio.windows_events import NULL
from pickle import FALSE
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

import json


baseUrl = "https://www.30book.com"
total_book = 137360


# excel_col_title = ['نام کتاب', 'دسته بندی', 'قیمت', 'ویژگی']

# # ? create instance from ecxel class
# excel = ExcelClass('excel/30_book.xlsx', excel_col_title)
# excel.addSheet('book', 0)

# ? get 20,0000 data
def get_a_thousand(twenty_thousand):

    for book_index in range(5000):
        sleep(0.3)
        # if (threading.active_count() < 400):

        # print('number of active thread is: ' + str(threading.active_count()))
        index = str(((twenty_thousand)*5000) + (book_index+1))
        print('getting index '+ index)
        thread = BookThreadClass(index)
        thread.start()

        # else:
        #     sleep(10)


def save_json(file_name, json_array):
    with open(file_name, 'w') as f:
        json.dump(json_array, f, ensure_ascii=False)

    print('json file saved')

# ? set interval to log active thread count every 1 second
def interval():
    file_index = 0
    while True:
        sleep(1 - time() % 1)

        if (threading.active_count() <= 2):

            json_name = 'final-data/book_5000_10000.json'
            save_json(json_name, json_array)


            if (file_index<0):
                file_index += 1
                get_a_thousand(file_index)

            else:
                break


        print('number of active thread is: ' + str(threading.active_count()))

class BookThreadClass (threading.Thread):
   def __init__(self, book_index):
      threading.Thread.__init__(self)
      self.book_index = book_index
   def run(self):
      return get_book_info(int(self.book_index))


# ? dictionary template
def create_dictionary():
    # Data to be written
    dictionary = {
        "id" : "" ,
        "URL" : "" ,
        "title" : "" ,
        "price" : "" ,
        "description" : "" ,
        "image" : "" ,
        "description" : "" ,
        "properties" : {
            "goodsType" : "",
            "category" : "" ,
            "mainSubject" : {
                "name" : "" ,
                "URL" : "" 
            },
            "subSubject" : {
                "name" : "" ,
                "URL" : "" 
            }
            ,
            "author": [
                {
                    "name" : "" ,
                    "URL" : "" 
                }
            ],
            "translator" : [
                {
                    "name" : "" ,
                    "URL" : "" 
                }
            ],
            "publisher" : {
                "name" : "" ,
                "URL" : "" 
            },
            "isbn" : "" ,
            "language" : "" ,
            "cutofBook" : "" ,
            "cover" : "" ,
            "pageCount" : "" ,
            "weight" : "" ,
            "published" : "" ,
            "publishedYear" : ""
        }
    }

    return dictionary



# ? map li tag to it text
def get_text(li):
    return li.get_text().strip()
  

# ? find attribute value base on persian name
def find_attribute(persian_title, key_list, value_list):
    try:
        key_list_mapped = list(map(get_text, key_list))
        index = key_list_mapped.index(persian_title)

        if (persian_title == 'موضوع اصلی' or persian_title == 'موضوع فرعی' or persian_title == 'نشر'):

            key_value_object = {
                "name" : (value_list[index]).get_text().strip() ,
                "URL" : baseUrl + value_list[index].find("a").get('href')
            }

            return key_value_object

        elif (persian_title == 'وزن'):
            try:
                return (value_list[index]).get_text().strip().replace(' گرم', '')
            except:
                return (value_list[index]).get_text().strip()

        elif (persian_title == 'تعداد صفحه'):
            try:
                return (value_list[index]).get_text().strip().replace(' صفحه', '')
            except:
                return (value_list[index]).get_text().strip()



        elif (persian_title == 'نویسنده' or persian_title == 'مترجم'):

            key_value_array = []
            for a_tag in value_list[index].find_all("a"):

                key_value_object = {
                    "name" : a_tag.get_text().strip() ,
                    "URL" : baseUrl + a_tag.get('href')
                }
                key_value_array.append(key_value_object)

            return key_value_array

        return (value_list[index]).get_text().strip()
    except:
        return None

json_array = []
 


def get_book_info(book_index):
    try:
        url = baseUrl + '/book/' + str(book_index)
        book_detail_html = requests.get(url)
        beauty_html = BeautifulSoup(book_detail_html.text, 'html.parser')

        book_title = beauty_html.find(class_='product-name').get_text()
        attribute_container = beauty_html.find(class_='uk-switcher')


        index = 0
        attribute_key = []
        attribute_value = []

        # ? have tow col for attrs
        for attribute_column in attribute_container.find_all(class_="uk-grid-collapse"):


            # ? have tow ul for attrs (first for key, second for value)
            for ul in attribute_column.find_all("ul"):

                for li in ul.find_all("li"):
                    attr = li.get_text().strip()

                    # ? for key
                    if index%2 == 0:
                        attribute_key.append(li)
                    # ? for value
                    else:
                        attribute_value.append(li)


                index += 1


        price = ''

        try:
            price = beauty_html.find(class_='product-slash-price').get_text().replace('\n', '')
        except:
            price = None

        description = ''

        try:
            description = beauty_html.find(class_='product-description-section-text').get_text().strip()
        except:
            description = None

        image = 'https://www.30book.com/Media/Book/' + str(book_index) + '.jpg'

        # try:
        #     image = baseUrl + beauty_html.find(class_='fluid-image').get('src')
        # except:
        #     image = None
        

        # excel.storeDataInExcel('book', row, 0, book_title, '', price, string_attribute)
        # row += 1

        book_dic = create_dictionary()


        book_dic["title"] = book_title
        book_dic["price"] = price
        book_dic["URL"] = url
        book_dic["id"] = str(book_index)
        book_dic["description"] = description
        book_dic["image"] = image



        book_dic["properties"]["goodsType"] = find_attribute('دسته بندی', attribute_key, attribute_value)
        book_dic["properties"]["category"] = find_attribute('نوع کالا', attribute_key, attribute_value)
        book_dic["properties"]["isbn"] = find_attribute('شابک', attribute_key, attribute_value)
        book_dic["properties"]["language"] = find_attribute('زبان کتاب', attribute_key, attribute_value)
        book_dic["properties"]["cutofBook"] = find_attribute('قطع کتاب', attribute_key, attribute_value)
        book_dic["properties"]["cover"] = find_attribute('جلد کتاب', attribute_key, attribute_value)
        book_dic["properties"]["pageCount"] = find_attribute('تعداد صفحه', attribute_key, attribute_value)
        book_dic["properties"]["weight"] = find_attribute('وزن', attribute_key, attribute_value)
        book_dic["properties"]["published"] = find_attribute('نوبت چاپ', attribute_key, attribute_value)
        book_dic["properties"]["publishedYear"] = find_attribute('سال انتشار', attribute_key, attribute_value)

        book_dic["properties"]["mainSubject"] = find_attribute('موضوع اصلی', attribute_key, attribute_value)
        book_dic["properties"]["subSubject"] = find_attribute('موضوع فرعی', attribute_key, attribute_value)
        book_dic["properties"]["publisher"] = find_attribute('نشر', attribute_key, attribute_value)
        book_dic["properties"]["author"] = find_attribute('نویسنده', attribute_key, attribute_value)
        book_dic["properties"]["translator"] = find_attribute('مترجم', attribute_key, attribute_value)


        json_array.append(book_dic)


        return book_dic
    except:
        print('can not get index ' + str(book_index+1))
        # return ''






# ! entry point
get_a_thousand(1)

interval()


# excel.closeExcel()


