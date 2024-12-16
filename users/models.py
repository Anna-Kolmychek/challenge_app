from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from config import constants
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """Model for custom user"""

    telegram_id = models.PositiveBigIntegerField(
        primary_key=True,
        verbose_name=_('telegra_id'),
    )
    username = models.CharField(
        max_length=constants.MAX_USERNAME_LENGTH,
        null=True,
        blank=True,
        verbose_name=_('username'),
    )

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.telegram_id}'
