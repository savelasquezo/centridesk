from django.db import models


class Accounts(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=255, unique=True)
    plan_id = models.CharField(max_length=255, null=False)
    expiration_date = models.BigIntegerField(null=True, default=None)
    renew = models.BooleanField(null=False, default=True)
    company = models.TextField(max_length=500, null=True, default=None)
    country = models.TextField(max_length=500, null=True, default=None)
    phone = models.TextField(max_length=20, null=True, default=None)
    web_page = models.TextField(max_length=500, null=True, default=None)
    active = models.BooleanField(null=False)
    created_at = models.BigIntegerField(null=False)
    updated_at = models.BigIntegerField(null=True, default=None)
    deactivated_at = models.BigIntegerField(null=True, default=None)

    def __str__(self):
        return self.unique_id

    class Meta:
        db_table = "api_accounts"
