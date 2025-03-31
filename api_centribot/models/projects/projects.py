from django.db import models


class Projects(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(default=None)
    dialog_flow_id = models.CharField(max_length=200, default=None)
    lang = models.CharField(max_length=200, default=None)
    account_id = models.CharField(max_length=200, null=True, default=None)
    timezone = models.CharField(max_length=255, null=True, default=None)
    active = models.BooleanField(default=True)
    sandbox = models.BooleanField(default=False)
    sandbox_id = models.CharField(max_length=255, null=True, default=None)
    created_at = models.BigIntegerField(default=None)
    updated_at = models.BigIntegerField(null=True)
    deactivated_at = models.BigIntegerField(null=True)

    class Meta:
        db_table = "api_projects"
