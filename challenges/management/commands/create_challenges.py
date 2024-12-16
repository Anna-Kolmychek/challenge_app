from django.core.management import BaseCommand

from challenges.management.data.challenges_data import challenges_data
from challenges.models import Challenge
from users.models import CustomUser


class Command(BaseCommand):
    """Create test Challenges"""

    def handle(self, *args, **options):
        count = 0

        for challenge_data in challenges_data.values():
            user = CustomUser.objects.filter(telegram_id=challenge_data.get('user')).first()
            challenge_data['user'] = user
            if not user:
                self.stdout.write(self.style.ERROR('User from challenge_data not found'))
                continue
            challenge, is_created = Challenge.objects.get_or_create(**challenge_data)

            if is_created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} challenges successfully created.'))
