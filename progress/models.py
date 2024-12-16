from django.db import models
from django.utils.translation import gettext as _

from challenges.models import Challenge


class Progress(models.Model):
    progress = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('progresses'),
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name=_('date'),
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name=_('challenge'),
    )

    class Meta:
        verbose_name = _('progress')
        verbose_name_plural = _('progresses')

    def __str__(self):
        return f'{self.progress} - {self.date} - {self.challenge.description}'
