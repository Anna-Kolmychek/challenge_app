from django.core.management import BaseCommand

from users.management.data.users_data import users_data
from users.models import CustomUser


class Command(BaseCommand):
    """Create admin and test user"""

    def handle(self, *args, **options):

        # Create admin
        if CustomUser.objects.filter(telegram_id=0).exists():
            self.stdout.write(self.style.WARNING(
                f'Admin already exists.'
            ))
        else:
            CustomUser.objects.create_superuser(
                telegram_id=0,
                password='0',
            )
            self.stdout.write(self.style.SUCCESS('Admin successfully created.'))

        # Create test users
        for user_data in users_data:
            if CustomUser.objects.filter(telegram_id=user_data.get('id')).exists():
                self.stdout.write(self.style.WARNING(
                    f'User {user_data.get("id")} already exists.'
                ))
                continue
            CustomUser.objects.create_user(
                telegram_id=user_data.get('id'),
                username=user_data.get('username'),
            )
            self.stdout.write(self.style.SUCCESS(
                f'User {user_data.get("id")} successfully created.'
            ))

