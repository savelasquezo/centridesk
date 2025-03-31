import phonenumbers

from shared.exceptions.invalid_value import InvalidValue
from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue


class Phone:

    def __init__(self, phone):
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if not isinstance(phone, str):
            raise TypeErrorValue('phone')

        phone = phone.strip()
        if not phone:
            raise RequiredValue('phone')

        if not phone.startswith("+"):
            raise InvalidValue('phone')

        try:
            phone_formatter = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(phone_formatter):
                phone = phonenumbers.format_number(phone_formatter, phonenumbers.PhoneNumberFormat.E164)
            else:
                raise InvalidValue('phone')
        except Exception:
            raise InvalidValue('phone')

        self.__phone = phone
