from django.contrib import admin

from tg_bot.models import InitData


@admin.register(InitData)
class InitDataAdmin(admin.ModelAdmin):
    pass
