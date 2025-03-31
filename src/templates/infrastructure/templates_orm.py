from api_centribot.models.whatsapp_templates.whatsapp_templates import WhatsappTemplates
from api_centribot.serializers.whatsapp_templates.whatsapp_templates import WhatsappTemplatesSerializerByModel


class TemplatesOrm:

    def __init__(self, project_id=None, projects_id=None, status=None):
        self.project_id = project_id
        self.projects_id = projects_id
        self.status = status

    def get_by_project_id_and_status(self):
        return [WhatsappTemplatesSerializerByModel(t).data for t in
                WhatsappTemplates.objects.filter(project_id=self.project_id, status=self.status)]

    def get_in_projects_id_and_status(self):
        return [WhatsappTemplatesSerializerByModel(t).data for t in
                WhatsappTemplates.objects.filter(project_id__in=self.projects_id, status=self.status)]
