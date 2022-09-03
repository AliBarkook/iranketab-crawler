
class BookClass:

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
    def __init__(self, title, category, attr):

        self.title = title
        self.category = category
        self.attr = attr
 