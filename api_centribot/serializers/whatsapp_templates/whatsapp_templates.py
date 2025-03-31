from rest_framework import serializers

from api_centribot.models.whatsapp_templates.whatsapp_templates import WhatsappTemplates
from api_centribot.serializers.shared.datetime_serializer import DateTimeFormat
from api_centribot.serializers.shared.decode_b64 import B64DecodeText


class WhatsappTemplatesSerializerByModel(serializers.ModelSerializer):
    id = serializers.UUIDField(source='unique_id')
    header = B64DecodeText()
    body = B64DecodeText()
    footer = B64DecodeText()
    buttons = B64DecodeText()
    created_at = DateTimeFormat()

    class Meta:
        model = WhatsappTemplates
        fields = ('id', 'project_id', 'category', 'name', 'language', 'header', 'body', 'footer', 'buttons', 'status',
                  'parameters_count', 'created_at')
