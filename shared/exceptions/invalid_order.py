from shared.exceptions.invalid_value import InvalidValue


class InvalidOrder(InvalidValue):

    def __init__(self):
        super().__init__(value='order')
