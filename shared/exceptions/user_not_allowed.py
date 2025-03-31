class UserNotAllowed(Exception):

    def __init__(self):
        self.message = "User not allowed"
        super().__init__(self.message)

    def __str__(self):
        return self.message
