class RequiredValue(Exception):

    def __init__(self, value, message="Required Value"):
        self.value = value
        self.message = f"{self.value.capitalize()} is required" if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
