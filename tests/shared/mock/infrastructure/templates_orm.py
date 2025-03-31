from tests.shared.mock.data import MockData


class TemplatesOrm:

    def __init__(self, project_id=None, projects_id=None, status=None, mock=None):
        self.project_id = project_id
        self.projects_id = projects_id
        self.status = status

        self.__mock = mock or MockData()

    def get_by_project_id_and_status(self):
        return [self.__format_template(template) for template in self.__mock.templates
                if template['project_id'] == self.project_id and template['status'] == self.status]

    def get_in_projects_id_and_status(self):
        return [self.__format_template(template) for template in self.__mock.templates
                if template['project_id'] in self.projects_id and template['status'] == self.status]

    @staticmethod
    def __format_template(template):
        return {
            "id": template['unique_id'],
            "project_id": template['project_id'],
            "category": template['category'],
            "name": template['name'],
            "language": template['language'],
            "header": template['header'],
            "body": template['body'],
            "footer": template['footer'],
            "buttons": template['buttons'],
            "parameters_count": template['parameters_count'],
            "status": template['status'],
            "created_at": template['created_at']
        }
