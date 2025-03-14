import calendar
from datetime import timedelta, date

from django.db import models
from django.db.models import Sum, Case, When, Value
from django.utils import timezone
from rest_framework import exceptions

from challenges.models import Challenge, Period, Progress


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
        started_date = get_period_start_date_month(started_at, year, month)
    return started_date


def get_period_start_date_month(start_date, period_year, period_month):
    """Get date when period started for monthly challenges"""
    start_day = start_date.day
    try:
        period_start_at = date(
            period_year,
            period_month,
            start_day
        )
    except ValueError:
        period_start_at = date(
            period_year,
            period_month,
            calendar.monthrange(period_year, period_month)[1]
        )
    return period_start_at


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
        if started_at.day > timezone.now().day:
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1
        period_finished_at = get_period_end_date_month(started_at, year, month)

    if finished_at and period_finished_at:
        period_finished_at = min(period_finished_at, finished_at)
    return period_finished_at


def get_period_end_date_month(start_date, period_year, period_month):
    """Get date when period will be finished for monthly challenges."""
    period_month += 1
    if period_month == 13:
        period_month = 1
        period_year += 1

    period_end_at = get_period_start_date_month(
        start_date, period_year, period_month
    ) - timedelta(days=1)

    return period_end_at


def get_current_progress(challenge):
    """Get current progress"""

    period_started_at = get_period_started_at(
        period=challenge.period,
        started_at=challenge.started_at
    )
    if not period_started_at:
        raise exceptions.ValidationError(
            {
                'started_at': f'The challenge{challenge.id} '
                              f'has problems with the start date.'}
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


def get_challenge_end_date(challenge):
    """Get finish date for challenge or current date"""
    if challenge.finished_at and challenge.finished_at < timezone.now().date():
        end_date = challenge.finished_at
    else:
        end_date = timezone.now().date()
    return end_date
