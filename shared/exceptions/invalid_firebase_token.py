class InvalidFirebaseToken(Exception):

    def __init__(self, value, message="Invalid User Token"):
        self.value = value
        self.message = f"{self.value} is an invalid token." if self.value else message
        super().__init__(self.message)

    def __str__(self):
        return self.message
