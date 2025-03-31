from rest_framework import serializers

from api.models.tickets.ticket_priorities import TicketPriorities


class PrioritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriorities
        fields = ('id', 'name', 'sort')
