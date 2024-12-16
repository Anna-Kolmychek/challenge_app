from django.db import models
from django.utils.translation import gettext as _

from config import constants
from users.models import CustomUser


class Period:
    """Possible periods"""
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


PERIOD_CHOICES = (
    (Period.DAY, _('day')),
    (Period.WEEK, _('week')),
    (Period.MONTH, _('month')),
)


class Challenge(models.Model):
    """Model for challenge"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='challenges',
        verbose_name=_('user'),
    )
    description = models.CharField(
        max_length=constants.MAX_CHAR_LENGTH,
        verbose_name=_('description'),
    )
    goal = models.PositiveSmallIntegerField(
        verbose_name=_('goal'),
    )
    period = models.CharField(
        max_length=constants.MAX_PERIOD_LENGTH,
        choices=PERIOD_CHOICES,
        verbose_name=_('period'),
    )
    started_at = models.DateField(
        verbose_name=_('started at'),
    )
    finished_at = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('finished at'),
    )
    is_finished = models.BooleanField(
        default=False,
        verbose_name=_('is finished'),
    )

    class Meta:
        verbose_name = _('challenge')
        verbose_name_plural = _('challenges')

    def __str__(self):
        return self.description
