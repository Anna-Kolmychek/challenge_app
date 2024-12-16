from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'is_superuser',)
    fields = (
        'telegram_id',
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
    )
