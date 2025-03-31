from django.db import models


class Accounts(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(null=False, default=True)

    @staticmethod
    def is_authenticated():
        return True
