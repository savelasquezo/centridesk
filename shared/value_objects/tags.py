from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.tag import Tag


class Tags:

    def __init__(self, tags):
        self.__name = 'tags'
        self.tags = tags

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        if not isinstance(tags, list):
            raise TypeErrorValue(self.__name)

        self.__tags = [Tag(tag).tag for tag in tags]
