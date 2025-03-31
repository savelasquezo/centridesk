from rest_framework import serializers

from api_centribot.models.projects.projects import Projects
from api_centribot.serializers.shared.datetime_serializer import DateTimeFormat


class ProjectSerializerByModel(serializers.ModelSerializer):
    id = serializers.UUIDField(source='unique_id')
    created_at = DateTimeFormat()
    updated_at = DateTimeFormat()
    deactivated_at = DateTimeFormat()
    origin_id = serializers.Field(default=None)

    class Meta:
        model = Projects
        fields = ('id', 'name', 'description', 'lang', 'account_id', 'timezone', 'active', 'sandbox',
                  'sandbox_id', 'origin_id', 'created_at', 'updated_at', 'deactivated_at')
