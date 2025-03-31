from time import strptime
from shared.exceptions.invalid_format import InvalidFormat
from shared.exceptions.invalid_type import InvalidType
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class InfoDownloadUseReport:

    def __init__(self, from_date, to_date) -> None:
        self.from_date = from_date
        self.to_date = to_date

    @property
    def data(self):
        return {
            'from': self.from_date,
            'to': self.to_date
        }

    @property
    def from_date(self):
        return self.__from
    
    @from_date.setter
    def from_date(self, value):
        if not isinstance(value, str):
            raise TypeErrorValue('from')
        
        from_date_formatted = value.strip()

        if not from_date_formatted:
            raise RequiredValue('from')
        
        try:
            strptime(value, '%Y-%m-%d')
        except Exception:
            raise InvalidFormat('from')
        
        self.__from = value
        
    @property
    def to_date(self):
        return self.__to
    
    @to_date.setter
    def to_date(self, value):
        if not isinstance(value, str):
            raise TypeErrorValue('to')
        
        to_date_formatted = value.strip()

        if not to_date_formatted:
            raise RequiredValue('to')
        
        try:
            strptime(value, '%Y-%m-%d')
        except Exception:
            raise InvalidFormat('to')
        
        self.__to = value
