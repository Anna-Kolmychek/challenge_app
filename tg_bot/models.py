from django.db import models
from rest_framework.utils import timezone


class InitData(models.Model):
    text = models.TextField(null=True, blank=True)
    datetime = models.DateField(default=timezone.now,)
