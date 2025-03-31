from shared.exceptions.generic import GenericException


class Paginator:

    def __init__(self, page, page_size, element=None, total=None, results=None):
        self.page = page
        self.page_size = page_size
        self.total = total
        self.results = results
        self.element = element

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page):
        page = int(page) if page is not None and page.isnumeric() else 1
        if page == 0:
            raise GenericException('That page number is less than 1')
        self.__page = page

    @property
    def page_size(self):
        return self.__page_size

    @page_size.setter
    def page_size(self, page_size):
        self.__page_size = int(page_size) if page_size is not None and page_size.isnumeric() else 100

    def get_response(self):
        next_page = None
        previous_page = None
        if self.page and self.page_size is not None:
            num_pages = int(self.total / self.page_size)
            last_page = num_pages if self.total % self.page_size == 0 else num_pages + 1

            next_page = self.page + 1 if self.page != last_page and self.page < last_page else None
            previous_page = last_page if not self.results else self.page - 1 if self.page != 1 else None

        return {
            self.element: self.results,
            'next_page': next_page,
            'previous_page': previous_page,
            'count': self.total
        }
