from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.type_error import TypeErrorValue


class ExternalID:

    def __init__(self, external_id):
        self.__name = 'external ID'
        self.external_id = external_id

    @property
    def external_id(self):
        return self.__external_id

    @external_id.setter
    def external_id(self, external_id):
        if not isinstance(external_id, str):
            raise TypeErrorValue(self.__name)

        external_id = external_id.strip()
        if not external_id:
            raise InvalidValue(self.__name)

        self.__external_id = external_id
