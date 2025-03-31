from string import capwords


class NotFound(Exception):

    def __init__(self, value=None, message="Not found."):
        self.message = f"{capwords(value)} not found" if value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
