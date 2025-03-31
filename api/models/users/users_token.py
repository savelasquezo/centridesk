from django.db import models


class UsersToken(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    centribot_user_id = models.CharField(max_length=255, default=None)
    mobile_id = models.TextField(default=None, null=True)
    created_at = models.BigIntegerField(default=None)
    updated_at = models.BigIntegerField(default=None, null=True)
