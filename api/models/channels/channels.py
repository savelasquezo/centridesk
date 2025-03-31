from django.db import models


class Channels(models.Model):
    objects = models.Manager()

    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    created_at = models.BigIntegerField()
    active = models.BooleanField(default=True)
