from shared.exceptions.not_found import NotFound


class GetTemplates:

    def __init__(self, account_id, project_id, accounts_platform_products_orm, projects_orm,
                 templates_orm, webhooks_orm):
        self.account_id = account_id
        self.project_id = project_id
        self.accounts_platform_products_orm = accounts_platform_products_orm
        self.projects_orm = projects_orm
        self.templates_orm = templates_orm
        self.webhooks_orm = webhooks_orm

        self.__approved_status = 'approved'

    def get_templates(self):
        self.accounts_platform_products_orm.account_id = self.account_id
        platform_products = self.accounts_platform_products_orm.get_by_id()

        campaigns = bool(platform_products and platform_products['centripush'])

        output = {
            "campaigns": campaigns,
            "token": None,
            "templates": []
        }

        if campaigns:
            # get webhook token
            self.webhooks_orm.account_id = self.account_id
            output['token'] = self.webhooks_orm.get_by_account().get('token', None)

            # If project_id, check if is from that account
            self.projects_orm.account_id = self.account_id
            self.projects_orm.project_id = self.project_id

            self.templates_orm.status = self.__approved_status

            if self.project_id:
                if not self.projects_orm.check_project_belows_account():
                    raise NotFound("project")

                self.templates_orm.project_id = self.project_id
                output['templates'] = self.templates_orm.get_by_project_id_and_status()

            else:
                account_projects = self.projects_orm.get_by_account_id()
                self.templates_orm.projects_id = [ap['id'] for ap in account_projects]
                output['templates'] = self.templates_orm.get_in_projects_id_and_status()

        return output
