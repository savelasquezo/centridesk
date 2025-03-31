class TooLongString(Exception):

    def __init__(self, value, max_characters=None, message="Too Long String"):
        self.value = value
        self.max_characters = max_characters

        self.message = f"{self.value.capitalize()} exceed the number of characters." if self.value else message

        if self.max_characters:
            self.message += f" Max: {self.max_characters}."

        super().__init__(self.message)

    def __str__(self):
        return self.message
