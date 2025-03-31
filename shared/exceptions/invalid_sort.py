from shared.exceptions.invalid_value import InvalidValue


class InvalidSort(InvalidValue):

    def __init__(self):
        super().__init__(value='sort')
