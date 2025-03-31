from shared.exceptions.generic import GenericException


class MobileId:
    def __init__(self, mobile_id):
        self.__str = 'Mobile id'
        self.mobile_id = mobile_id

    @property
    def mobile_id(self):
        return self.__mobile_id

    @mobile_id.setter
    def mobile_id(self, mobile_id):
        if not isinstance(mobile_id, str):
            raise GenericException(f'{self.__str} has an invalid value')

        mobile_id = mobile_id.strip()
        if not mobile_id:
            raise GenericException(f'{self.__str} has an invalid value')

        self.__mobile_id = mobile_id
