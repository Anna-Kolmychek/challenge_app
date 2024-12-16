from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    """Create admin and test user"""

    def handle(self, *args, **options):
        try:
            CustomUser.objects.create_superuser(
                telegram_id=0,
                password='0',
            )
            self.stdout.write(self.style.SUCCESS('Admin successfully created.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Admin has not been created.'))
            self.stdout.write(self.style.ERROR(f'error: {e}'))

        try:
            CustomUser.objects.create_user(
                telegram_id=111,
                password='111',
            )
            self.stdout.write(self.style.SUCCESS('User 111 successfully created.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('User 111 has not been created.'))
            self.stdout.write(self.style.ERROR(f'error: {e}'))

