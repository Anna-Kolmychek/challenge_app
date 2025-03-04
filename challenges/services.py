import calendar
from datetime import timedelta, datetime, date

from django.db import models
from django.db.models import Sum, Case, When, Value
from django.utils import timezone
from rest_framework import exceptions

from challenges.models import Challenge, Period
from progress.models import Progress


def finish_completed_challenges(user):
    """Finish the completed challenges for the user"""

    challenges = Challenge.objects.filter(
        user=user,
        is_finished=False,
        finished_at__lt=timezone.now()
    ).all()

    return challenges.update(is_finished=True)


def get_period_started_at(period, started_at):
    """Get date when current period started"""

    started_date = None

    if period == Period.DAY:
        started_date = timezone.now().date()
    elif period == Period.WEEK:
        full_weeks = (timezone.now().date() - started_at).days // 7
        started_date = started_at + timedelta(weeks=full_weeks)
    elif period == Period.MONTH:
        year = timezone.now().year
        month = timezone.now().month
        if started_at.day > timezone.now().day:
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1
        try:
            started_date = datetime(
                year,
                month,
                started_at.day
            )
        except ValueError:
            started_date = datetime(
                year,
                month,
                calendar.monthrange(year, month)[1]
            )
    return started_date


def get_period_finished_at(started_at, finished_at, period):
    """Get date when current period will be finished"""
    period_finished_at = None

    if period == Period.DAY:
        period_finished_at = timezone.now().date()

    if period == Period.WEEK:
        full_weeks = (timezone.now().date() - started_at).days // 7 + 1
        period_finished_at = started_at + timedelta(days=full_weeks * 7 - 1)

    if period == Period.MONTH:
        year = timezone.now().year
        month = timezone.now().month
        if started_at.day < timezone.now().day:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
        try:
            period_finished_at = date(
                year,
                month,
                started_at.day-1
            )
        except ValueError:
            period_finished_at = date(
                year,
                month,
                calendar.monthrange(year, month)[1]-1
            )

    if finished_at and period_finished_at:
        period_finished_at = min(period_finished_at, finished_at)
    return period_finished_at


def get_current_progress(challenge):
    """Get current progress"""

    period_started_at = get_period_started_at(
        period=challenge.period,
        started_at=challenge.started_at
    )
    if not period_started_at:
        raise exceptions.ValidationError(
            {
                'started_at': f'The challenge{challenge.id} has problems with the start date.'}
        )
    current_progress = Progress.objects.filter(
        challenge=challenge, date__gte=period_started_at
    ).aggregate(sum=Sum('progress'))
    return current_progress.get('sum') if current_progress.get('sum') else 0


def reduce_current_progress(challenge, del_progress):
    """Reduce current progress"""

    progresses = Progress.objects.filter(challenge=challenge).order_by('-date')

    total_progress = 0
    progresses_to_delete = []

    for progress in progresses:
        if total_progress + progress.progress <= del_progress:
            total_progress += progress.progress
            progresses_to_delete.append(progress.id)
        else:
            remain = del_progress - total_progress
            progress.progress -= remain
            progress.save()
            break

    if progresses_to_delete:
        Progress.objects.filter(id__in=progresses_to_delete).delete()


def custom_ordering(challenges):
    """Custom ordering for list of challenges.
    first active challenges, after with a start date in the future
    inside first with a period of a day, then a week, then a month,
    inside the  alphabetical description"""

    current_date = timezone.now().date()

    sorted_challenges = challenges.annotate(
        period_order=Case(
            When(period=Period.DAY, then=Value(1)),
            When(period=Period.WEEK, then=Value(2)),
            When(period=Period.MONTH, then=Value(3)),
            default=Value(4),
            output_field=models.IntegerField(),
        ),
        started_order=Case(
            When(started_at__lt=current_date, then=Value(1)),
            When(started_at__gte=current_date, then=Value(2)),
            default=Value(3),
            output_field=models.IntegerField(),
        )
    ).order_by(
        'started_order',
        'period_order',
        'description'
    )
    return sorted_challenges
