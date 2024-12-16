from django.contrib import admin

from challenges.models import Challenge


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'description',
        'period',
        'started_at',
        'finished_at',
        'is_finished',
    )
    list_display_links = ('description', )
    fields = (
        'id',
        'user',
        'description',
        ('goal', 'period',),
        ('started_at', 'finished_at',),
        'is_finished',
    )
    readonly_fields = ('id', )
    list_filter = ('period', 'is_finished', )
