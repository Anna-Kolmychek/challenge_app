from django.core.management import BaseCommand

from challenges.models import Challenge
from progress.management.data.progress_data import progresses_data
from progress.models import Progress


class Command(BaseCommand):
    """Create test progress"""

    def handle(self, *args, **options):
        count = 0

        for common_data in progresses_data.values():
            challenge = Challenge.objects.filter(description=common_data.get('challenge')).first()
            is_progress_exists = Progress.objects.filter(challenge=challenge).exists()
            if not challenge or is_progress_exists:
                continue

            for progress_data in common_data.get('progresses'):
                progress_data['challenge'] = challenge
                Progress.objects.create(**progress_data)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} progress records successfully created.'))
