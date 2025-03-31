from django.core.exceptions import ObjectDoesNotExist

from api.models.tickets.ticket_priorities import TicketPriorities
from api.serializers.tickets.priorities import PrioritiesSerializer
from shared.exceptions.not_found import NotFound


class PrioritiesOrm:
    def __init__(self, priority_id=None, name=None):
        self.priority_id = priority_id
        self.name = name

    def get_by_id(self):
        try:
            priority = TicketPriorities.objects.get(pk=self.priority_id)

        except ObjectDoesNotExist:
            raise NotFound('priority')

        return PrioritiesSerializer(priority).data

    def get_by_name(self):
        try:
            priority = TicketPriorities.objects.get(name=self.name)

        except ObjectDoesNotExist:
            raise NotFound('priority')

        return PrioritiesSerializer(priority).data

    @staticmethod
    def get_all():
        priorities = TicketPriorities.objects.filter().order_by('sort')
        return PrioritiesSerializer(priorities, many=True).data
