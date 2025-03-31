class GenericException(Exception):

    def __init__(self, message="Error"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
