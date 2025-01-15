import calendar
from datetime import timedelta, datetime

from django.utils import timezone

from challenges.models import Challenge, Period


def finish_completed_challenges(user):
    """Finish the completed challenges for the user"""

    challenges = Challenge.objects.filter(
        user=user,
        is_finished=False,
        finished_at__lt=timezone.now()
    ).all()

    return challenges.update(is_finished=True)


def get_started_date_for_current_progress(period, started_at):
    """Get the start date to calculate the current progress"""

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
