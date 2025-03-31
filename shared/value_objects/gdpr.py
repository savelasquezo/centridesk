from shared.exceptions.type_error import TypeErrorValue


class Gdpr:

    def __init__(self, gdpr):
        self.__name = 'gdpr'
        self.gdpr = gdpr

    @property
    def gdpr(self):
        return self.__gdpr

    @gdpr.setter
    def gdpr(self, gdpr):
        if not isinstance(gdpr, bool):
            raise TypeErrorValue(self.__name)

        self.__gdpr = gdpr
