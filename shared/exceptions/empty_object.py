class EmptyObject(Exception):

    def __init__(self, value, message="Empty Object"):
        self.value = value
        self.message = f"{self.value.capitalize()} can not be empty." if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
