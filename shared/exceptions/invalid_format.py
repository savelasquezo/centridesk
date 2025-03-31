class InvalidFormat(Exception):

    def __init__(self, value, message="Invalid Format"):
        self.value = value
        self.message = f"{self.value.capitalize()} has an invalid format." if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
