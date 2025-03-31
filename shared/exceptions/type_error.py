class TypeErrorValue(Exception):

    def __init__(self, value, message="Invalid Type"):
        self.value = value
        self.message = f"{self.value.capitalize()} has an invalid type." if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
