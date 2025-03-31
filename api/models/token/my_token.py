from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class MyToken(Token):
    key = models.CharField(_("Key"), max_length=255, db_index=True, unique=True)

    user = models.ForeignKey(
        'api.accounts', related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("Account")
    )
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        unique_together = (('user', 'name'),)
