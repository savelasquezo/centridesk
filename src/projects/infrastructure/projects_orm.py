from api_centribot.models.projects.projects import Projects
from api_centribot.serializers.projects.projects import ProjectSerializerByModel


class ProjectsOrm:

    def __init__(self, account_id=None, project_id=None):
        self.account_id = account_id
        self.project_id = project_id

    def check_project_belows_account(self):
        return Projects.objects.filter(unique_id=self.project_id, account_id=self.account_id).exists()

    def get_by_account_id(self):
        return [ProjectSerializerByModel(p).data for p in Projects.objects.filter(account_id=self.account_id)]
