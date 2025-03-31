from django.db import models


class UsersAccounts(models.Model):
    objects = models.Manager()

    user_id = models.CharField(max_length=255, null=False)
    account_id = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "api_usersaccounts"
