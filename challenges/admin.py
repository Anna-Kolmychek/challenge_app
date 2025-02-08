from django.contrib import admin

from challenges.models import Challenge
from progress.models import Progress


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user',
        'description',
        'period',
        'started_at',
        'finished_at',
        'is_finished',
    )
    list_display_links = ('description', )
    fields = (
        'uuid',
        'user',
        'description',
        ('goal', 'period',),
        ('started_at', 'finished_at',),
        'is_finished',
    )
    readonly_fields = ('uuid', )
    list_filter = ('period', 'is_finished', )
