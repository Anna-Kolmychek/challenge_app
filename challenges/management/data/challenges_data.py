from datetime import timedelta

from django.utils import timezone

challenges_data = {
    1: {
        'user': 111,
        'description': 'Take at least 10,000 steps every day.',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=5),
        'finished_at': None,
        'is_finished': False,
    },
    2: {
        'user': 111,
        'description': 'Go to the gym 3 times a week.',
        'goal': 3,
        'period': 'week',
        'started_at': timezone.now() - timedelta(days=15),
        'finished_at': None,
        'is_finished': False,
    },
    3: {
        'user': 111,
        'description': 'Give up all sweets and foods with added sugar for a month.',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=10),
        'finished_at': timezone.now() + timedelta(days=20),
        'is_finished': False,
    },
    4: {
        'user': 111,
        'description': 'Read 3 books a month.',
        'goal': 3,
        'period': 'month',
        'started_at': timezone.now() - timedelta(days=40),
        'finished_at': None,
        'is_finished': False,
    },
    5: {
        'user': 111,
        'description': 'Spend a week without access to social media',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=10),
        'finished_at': timezone.now() - timedelta(days=4),
        'is_finished': True,
    },
    6: {
        'user': 111,
        'description': 'Do morning exercises every day',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=40),
        'finished_at': None,
        'is_finished': True,
    },
}
