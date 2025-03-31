from django.db import models


class UsersRoles(models.Model):
    objects = models.Manager()

    user_id = models.CharField(max_length=255, blank=True, editable=False)
    role_id = models.CharField(max_length=255, blank=True, editable=False)

    class Meta:
        db_table = "api_usersroles"
