from django.contrib import admin

from challenges.models import Challenge, Progress


class ProgressInline(admin.TabularInline):
    model = Progress
    fields = ('progress', 'date')
    extra = 0


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
    inlines = (ProgressInline, )
    readonly_fields = ('uuid', )
    list_filter = ('period', 'is_finished', )
    search_fields = ('user__telegram_id', )


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('progress', 'date', 'challenge', 'user', )
    list_filter = ('challenge__user', )
    search_fields = ('challenge__description', 'challenge__user__telegram_id', )
    fields = ('progress', 'date', 'challenge', )

    def user(self, obj):
        return obj.challenge.user