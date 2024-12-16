from django.contrib import admin

from progress.models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('progress', 'date', 'challenge', )
    fields = ('progress', 'date', 'challenge', )
    # readonly_fields = ('date', )
