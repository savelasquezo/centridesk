from tests.shared.mock.data import MockData


class ProjectsOrm:

    def __init__(self, account_id=None, project_id=None, mock=None):
        self.account_id = account_id
        self.project_id = project_id

        self.__mock = mock or MockData()

    def check_project_belows_account(self):
        for project in self.__mock.projects:
            if project['account_id'] == self.account_id and project['id'] == self.project_id:
                return True

        return False

    def get_by_account_id(self):
        return [project for project in self.__mock.projects if project['account_id'] == self.account_id]
