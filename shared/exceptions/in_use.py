class InUse(Exception):

    def __init__(self, value, message="In use"):
        self.value = value
        self.message = f"{self.value.capitalize()} is in use" if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
