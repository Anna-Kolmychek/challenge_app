from datetime import timedelta

from django.utils import timezone

challenges_data = [
    {
        'description': 'Take at least 10,000 steps every day.',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=5),
        'finished_at': None,
        'is_finished': False,
        'progresses': [
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=5),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=4),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=2),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=1),
            },
        ]
    },
    {
        'description': 'Go to the gym 3 times a week.',
        'goal': 3,
        'period': 'week',
        'started_at': timezone.now() - timedelta(days=19),
        'finished_at': None,
        'is_finished': False,
        'progresses': [
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=14),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=12),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=9),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=5),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=1),
            },
        ]
    },
    {
        'description': 'Give up all sweets and foods with added sugar for a month.',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=10),
        'finished_at': timezone.now() + timedelta(days=20),
        'is_finished': False,
        'progresses': [
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=10),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=9),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=5),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=3),
            },
            {
                'progress': 1,
                'date': timezone.now(),
            },
        ]
    },
    {
        'description': 'Read 3 books a month.',
        'goal': 3,
        'period': 'month',
        'started_at': timezone.now() - timedelta(days=40),
        'finished_at': None,
        'is_finished': False,
        'progresses': [
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=30),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=20),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=12),
            },
            {
                'progress': 1,
                'date': timezone.now() - timedelta(days=5),
            },
        ]
    },
    {
        'description': 'Spend a week without access to social media',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=10),
        'finished_at': timezone.now() - timedelta(days=4),
        'is_finished': True,
        'progresses': []
    },
    {
        'description': 'Do morning exercises every day',
        'goal': 1,
        'period': 'day',
        'started_at': timezone.now() - timedelta(days=40),
        'finished_at': timezone.now(),
        'is_finished': True,
        'progresses': []
    },
]
