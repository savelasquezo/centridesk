from shared.exceptions.invalid_value import InvalidValue


class InvalidFilter(InvalidValue):

    def __init__(self):
        super().__init__(value='filter')
