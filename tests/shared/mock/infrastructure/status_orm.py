from api.serializers.tickets.ticket_status import StatusSerializer
from shared.exceptions.not_found import NotFound
from tests.shared.mock.data import MockData


class StatusOrm:

    def __init__(self, status_id=None, name=None, mock=None):
        self.status_id = status_id
        self.name = name

        self.__mock = mock or MockData()

    def get_by_id(self):
        for k, v in self.__mock.status_dict.items():
            if k == self.status_id:
                return StatusSerializer({'id': k, 'name': v}).data

        raise NotFound('status')

    def get_by_name(self):
        for k, v in self.__mock.status_dict.items():
            if v == self.name:
                return StatusSerializer({'id': k, 'name': v}).data

        raise NotFound('status')

    def get_all(self):
        output = []
        for k, v in self.__mock.status_dict.items():
            output.append(StatusSerializer({'id': k, 'name': v}).data)
        return output
