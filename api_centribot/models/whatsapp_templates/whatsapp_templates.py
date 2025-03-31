from django.db import models


class WhatsappTemplates(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=255, unique=True)
    project_id = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    language = models.CharField(max_length=255, null=False)
    header = models.TextField(null=True)
    body = models.TextField()
    footer = models.TextField(null=True)
    buttons = models.TextField(null=True)
    status = models.CharField(max_length=255, null=False)
    parameters_count = models.BigIntegerField(null=False, default=0)
    created_at = models.BigIntegerField(null=False, default=None)
    requested_at = models.BigIntegerField(null=True, default=None)
    approved_at = models.BigIntegerField(null=True, default=None)
    rejected_at = models.BigIntegerField(null=True, default=None)

    class Meta:
        db_table = "api_whatsapptemplates"
