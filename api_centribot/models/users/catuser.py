from django.contrib.auth.models import User
from django.db import models


class CATUser(models.Model):
    objects = models.Manager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, blank=True, unique=True)
    lang = models.CharField(max_length=255, default=None, null=True)
    created_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)
    deactivated_at = models.IntegerField(null=True)

    class Meta:
        db_table = "api_catuser"
