class InvalidType(TypeError):

    def __init__(self, value, message="Type Error"):
        self.message = f"{value.capitalize()} has an invalid type." if value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
