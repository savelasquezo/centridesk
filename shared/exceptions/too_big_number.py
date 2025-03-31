class TooBigNumber(Exception):

    def __init__(self, value, max_number=None, message="Too Big Number"):
        self.value = value
        self.max_number = max_number

        self.message = f"{self.value} exceed the size." if self.value else message

        if self.max_number:
            self.message += f" Max: {self.max_number}."

        super().__init__(self.message)

    def __str__(self):
        return self.message
