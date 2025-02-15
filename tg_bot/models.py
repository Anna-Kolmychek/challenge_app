from django.db import models


class InitData(models.Model):
    text = models.TextField(null=True, blank=True)
    datetime = models.DateField(auto_now_add=True)

