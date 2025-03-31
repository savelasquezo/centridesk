from django.db import models


class TicketPriorities(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=255)
    sort = models.IntegerField(null=False, default=0)
