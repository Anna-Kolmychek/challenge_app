from datetime import timedelta

from django.utils import timezone

progresses_data = {
    1: {
        'challenge': 'Take at least 10,000 steps every day.',
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
    2: {
        'challenge': 'Go to the gym 3 times a week.',
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
    3: {
        'challenge': 'Give up all sweets and foods with added sugar for a month.',
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
    4: {
        'challenge': 'Read 3 books a month.',
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
}

