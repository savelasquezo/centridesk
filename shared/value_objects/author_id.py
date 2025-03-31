from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.unique_id import UniqueID


class AuthorID:
    def __init__(self, author_id):
        self.author_id = author_id

    @property
    def author_id(self):
        return self.__author_id

    @author_id.setter
    def author_id(self, author_id):
        value = None
        if author_id:
            try:
                author_id = UniqueID(author_id)
            except Exception:
                raise TypeErrorValue('author ID')
            value = author_id.value

        self.__author_id = value
