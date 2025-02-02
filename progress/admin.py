from django.contrib import admin

from progress.models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('progress', 'date', 'challenge', 'user', )
    list_filter = ('challenge__user', )
    search_fields = ('challenge__description', 'challenge__user__telegram_id', )
    fields = ('progress', 'date', 'challenge', )


    def user(self, obj):
        return obj.challenge.user

