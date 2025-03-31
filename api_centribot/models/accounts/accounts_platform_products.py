from django.db import models


class AccountsPlatformProducts(models.Model):
    objects = models.Manager()

    account_id = models.CharField(max_length=255, unique=True)
    centridesk = models.BooleanField(null=True, default=None)
    centripush = models.BooleanField(null=True, default=None)

    class Meta:
        db_table = "api_accountsplatformproducts"
