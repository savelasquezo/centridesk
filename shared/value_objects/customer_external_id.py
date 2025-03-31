from shared.value_objects.string import String


class CustomerExternalId:

    def __init__(self, external_id):
        self.__name = 'external id'
        self.external_id = external_id

    @property
    def external_id(self):
        return self.__external_id

    @external_id.setter
    def external_id(self, external_id):
        self.__external_id = String(name=self.__name, value=external_id, required=False)
