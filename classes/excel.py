
# ? import excel module
import xlsxwriter 

class ExcelClass:

    """

    |---------------------------------------------------------------------
    |                                                                    |
    |     excel Class                                                    |
    |                                                                    |
    |---------------------------------------------------------------------
    |                                                                    |
    |   1 - initial Class with excel name, sheet name and list of title  |
    |                                                                    |
    |   2 - create excel file and worksheet                              |
    |                                                                    |
    |   3 - close excel                                                  |
    |                                                                    |
    |   4 - store course data in excel row                               |
    |                                                                    |
    ----------------------------------------------------------------------

    """
    # ? -> 1
    def __init__(self, excelName, coursePropTitleList):

        self.excelName = excelName
        # self.sheetName = sheetName
        self.coursePropTitleList = coursePropTitleList

        self.excelFile = xlsxwriter.Workbook(excelName)
        self.worksheet = []
        # self.worksheet = self.excelFile.add_worksheet(sheetName)
    # ? -> 2
    # def initExcel(self):
    #     col = 0
    #     for title in self.coursePropTitleList:

    #         self.worksheet.write(0, col, title)
    #         col += 1
    # ? -> 3
    def closeExcel(self):
        while True:
            try:
                self.excelFile.close()
                print('excel file closed')
                break
            except xlsxwriter.exceptions.FileCreateError as e:
                decision = input("Exception caught in workbook.close(): %s\n"
                                "Please close the file if it is open in Excel.\n"
                                "Try to write file again? [Y/n]: " % e)
                if decision != 'n':
                    continue
    # ? -> 4
    def storeDataInExcel(self, sheet_name, row, col, book_name, category, book_price, attr):
        try:
            worksheet = self.excelFile.get_worksheet_by_name(sheet_name)
            # for prop in course.getCourseList():
            worksheet.write(row, col, book_name)
            col += 1
            worksheet.write(row, col, category)
            col += 1
            worksheet.write(row, col, book_price)
            col += 1
            worksheet.write(row, col, attr)
            col += 1
        except:
            print('can not write to excel file course number' + str(row))

    # ? -> 5
    def addSheet(self, sheet_name, index):
        # self.sheetName = sheetName
        self.worksheet.append(self.excelFile.add_worksheet(sheet_name))

        col = 0
        for title in self.coursePropTitleList:

            self.worksheet[index].write(0, col, title)
            col += 1
