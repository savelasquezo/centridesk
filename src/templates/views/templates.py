from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.shared.api_handler import api_handler
from api.shared.permissions_static_user_token import PermissionsStaticUserToken
from src.accounts.infrastructure.accounts_platform_products_orm import AccountsPlatformProductsOrm
from src.projects.infrastructure.projects_orm import ProjectsOrm
from src.templates.application.get_templates import GetTemplates
from src.templates.infrastructure.templates_orm import TemplatesOrm
from src.webhooks.infrastructure.webhooks_orm import WebhooksOrm


class TemplatesView(APIView):
    permission_classes = [IsAuthenticated | PermissionsStaticUserToken]

    @api_handler
    def get(self, request, **kwargs):
        app = GetTemplates(
            account_id=kwargs['account_id'],
            project_id=request.GET.get('centribot_project_id', None),
            accounts_platform_products_orm=AccountsPlatformProductsOrm(),
            projects_orm=ProjectsOrm(),
            templates_orm=TemplatesOrm(),
            webhooks_orm=WebhooksOrm()
        )
        return app.get_templates()
