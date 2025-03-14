import uuid
from django.db import models
from django.utils import timezone
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

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('uuid'),
    )
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
        ordering = ('user', 'description', )
        verbose_name = _('challenge')
        verbose_name_plural = _('challenges')

    def __str__(self):
        return self.description


class Progress(models.Model):
    """Model for Progress"""

    progress = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('progresses'),
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date'),
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name='progresses',
        verbose_name=_('challenge'),
    )

    class Meta:
        ordering = ('date', )
        verbose_name = _('progress')
        verbose_name_plural = _('progresses')

    def __str__(self):
        return f'{self.progress} - {self.date} - {self.challenge.description}'
