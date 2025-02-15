from django.db import models
from django.utils import timezone


class InitData(models.Model):
    text = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
