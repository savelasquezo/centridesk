from django.core.exceptions import ObjectDoesNotExist

from api.models.tickets.ticket_status import TicketStatus
from api.serializers.tickets.ticket_status import StatusSerializer
from shared.exceptions.not_found import NotFound


class StatusOrm:

    def __init__(self, status_id=None, name=None):
        self.status_id = status_id
        self.name = name

    def get_by_id(self):
        try:
            status = TicketStatus.objects.get(pk=self.status_id)

        except ObjectDoesNotExist:
            raise NotFound('status')

        return StatusSerializer(status).data

    def get_by_name(self):
        try:
            priority = TicketStatus.objects.get(name=self.name)

        except ObjectDoesNotExist:
            raise NotFound('status')

        return StatusSerializer(priority).data

    @staticmethod
    def get_all():
        priorities = TicketStatus.objects.filter().order_by('sort')
        return StatusSerializer(priorities, many=True).data
