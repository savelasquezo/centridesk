class Unauthorized(Exception):

    def __init__(self, value=None, message="No active account found with the given credentials"):
        self.message = value.capitalize() if value and isinstance(value, str) else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
