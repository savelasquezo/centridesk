from rest_framework import serializers

from api.models.tickets.ticket_status import TicketStatus


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name', 'sort')
