from shared.value_objects.string import String


class Delegation:

    def __init__(self, delegation):
        self.__name = 'delegation'
        self.delegation = delegation

    @property
    def delegation(self):
        return self.__delegation

    @delegation.setter
    def delegation(self, delegation):
        self.__delegation = String(name=self.__name, value=delegation, required=False)
