from api.serializers.tickets.priorities import PrioritiesSerializer
from shared.exceptions.not_found import NotFound
from tests.shared.mock.data import MockData


class PrioritiesOrm:

    def __init__(self, priority_id=None, name=None, mock=None):
        self.priority_id = priority_id
        self.name = name

        self.__mock = mock or MockData()

    def get_by_id(self):
        for k, v in self.__mock.priorities_dict.items():
            if k == self.priority_id:
                return PrioritiesSerializer({'id': k, 'name': v}).data

        raise NotFound('priority')

    def get_all(self):
        output = []
        for k, v in self.__mock.priorities_dict.items():
            output.append(PrioritiesSerializer({'id': k, 'name': v}).data)
        return output

    def get_by_name(self):
        for k, v in self.__mock.priorities_dict.items():
            if v == self.name:
                return PrioritiesSerializer({'id': k, 'name': v}).data

        raise NotFound('priority')
