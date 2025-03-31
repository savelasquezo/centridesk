from shared.value_objects.string import String


class Company:

    def __init__(self, company):
        self.__name = 'company'
        self.company = company

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = String(name=self.__name, value=company, required=False)
