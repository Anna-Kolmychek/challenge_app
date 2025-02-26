from django.core.management import BaseCommand

from challenges.management.data.challenges_data import challenges_data
from challenges.models import Challenge
from progress.models import Progress
from users.management.data.users_data import users_data
from users.models import CustomUser


class Command(BaseCommand):
    """Create test Challenges and Progress"""

    def handle(self, *args, **options):
        count = 0

        for user_data in users_data:
            user = CustomUser.objects.filter(
                telegram_id=user_data.get('id')
            ).first()

            if not user:
                self.stdout.write(self.style.ERROR(
                    f'User {user_data.get("id")} not found'
                ))
                continue

            for challenge_data in challenges_data:
                challenge_data['user'] = user

                if Challenge.objects.filter(
                        user=user, description=challenge_data.get('description')
                ).exists():
                    continue

                challenge_data_copy = challenge_data.copy()
                progresses = challenge_data_copy.pop('progresses')
                challenge = Challenge.objects.create(**challenge_data_copy)
                for progress in progresses:
                    progress['challenge'] = challenge
                    Progress.objects.create(**progress)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} challenges successfully created.'))
