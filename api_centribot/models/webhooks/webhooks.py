from django.db import models


class Webhooks(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=255, null=False)
    account_id = models.CharField(max_length=255, null=False)
    token = models.CharField(max_length=255, null=False)
    created_at = models.BigIntegerField(null=True)

    class Meta:
        db_table = "api_webhooks"
