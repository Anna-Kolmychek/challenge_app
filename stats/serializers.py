from datetime import datetime, timedelta

from django.db.models import Sum
from rest_framework import serializers
from django.utils import timezone

from challenges.models import Challenge, Period
from challenges.serializers import GetChallengeSerializer
from challenges.services import finish_completed_challenges


class CommonStatisticsSerializer(serializers.Serializer):
    days_since_registration = serializers.IntegerField(min_value=1)

    def to_representation(self, challenges):
        user = self.context.get('request').user

        days_since_registration = self._get_days_since_registration(user)
        count_all_challenges = self._get_count_all_challenges(challenges)
        count_completed_challenges = self._get_count_completed_challenges(challenges)

        longest_challenge_data = self._get_longest_challenge(challenges)
        longest_challenge = longest_challenge_data.get('longest_challenge')
        longest_challenge_duration = longest_challenge_data.get('longest_challenge_duration')

        effective_challenge = None
        effective_challenge_percent = 0.0

        periods_daily_data = self._get_count_periods_daily(
            challenges,
            effective_challenge,
            effective_challenge_percent
        )

        (
            count_all_periods_weekly,
            count_successfully_periods_weekly,
            effective_challenge,
            effective_challenge_percent,
        ) = self._get_count_periods_weekly(
            challenges,
            effective_challenge,
            effective_challenge_percent
        )

        (
            count_all_periods_monthly,
            count_successfully_periods_monthly,
            effective_challenge,
            effective_challenge_percent,
        ) = self._get_count_periods_monthly(
            challenges,
            effective_challenge,
            effective_challenge_percent
        )

        count_all_periods_daily = periods_daily_data.get('count_all_periods_daily')
        count_successfully_periods_daily = periods_daily_data.get('count_successfully_periods_daily')
        effective_challenge = periods_daily_data.get('effective_challenge')
        effective_challenge_percent = periods_daily_data.get('effective_challenge_percent')

        return {
            'days_since_registration': days_since_registration,

            'count_completed_challenges': count_completed_challenges,
            'count_all_challenges': count_all_challenges,

            'count_all_periods_daily': count_all_periods_daily,
            'count_successfully_periods_daily': count_successfully_periods_daily,

            'count_all_periods_weekly': count_all_periods_weekly,
            'count_successfully_periods_weekly': count_successfully_periods_weekly,

            'count_all_periods_monthly': count_all_periods_monthly,
            'count_successfully_periods_monthly': count_successfully_periods_monthly,

            'effective_challenge_percent': effective_challenge_percent,
            'effective_challenge': GetChallengeSerializer(effective_challenge).data,

            'longest_challenge_duration': longest_challenge_duration,
            'longest_challenge': GetChallengeSerializer(longest_challenge).data,

        }

    @staticmethod
    def _get_days_since_registration(user):
        return (timezone.now().date() - user.date_joined.date()).days + 1

    @staticmethod
    def _get_count_all_challenges(challenges):
        return len(challenges)

    @staticmethod
    def _get_count_completed_challenges(challenges):
        return challenges.filter(is_finished=True).count()

    @staticmethod
    def _get_longest_challenge(challenges):
        longest_challenge = None
        longest_challenge_duration = 0

        for challenge in challenges:
            end_date = challenge.finished_at if challenge.is_finished else timezone.now().date()
            duration = (end_date - challenge.started_at).days + 1

            if duration > longest_challenge_duration:
                longest_challenge_duration = duration
                longest_challenge = challenge

        return {
            'longest_challenge': longest_challenge,
            'longest_challenge_duration': longest_challenge_duration,
        }

    def _get_count_periods_daily(
            self, challenges, effective_challenge, effective_challenge_percent
    ):
        count_all_periods_daily = 0
        count_successfully_periods_daily = 0

        challenges = challenges.filter(period=Period.DAY).all()
        for challenge in challenges:
            periods, successful_periods = self._get_count_periods_daily_one_challenge(challenge)
            count_all_periods_daily += periods
            count_successfully_periods_daily += successful_periods

            percent = successful_periods / periods
            if percent > effective_challenge_percent:
                effective_challenge_percent = percent
                effective_challenge = challenge

        return {
            'count_all_periods_daily': count_all_periods_daily,
            'count_successfully_periods_daily': count_successfully_periods_daily,
            'effective_challenge': effective_challenge,
            'effective_challenge_percent': effective_challenge_percent,
        }

    @staticmethod
    def _get_count_periods_daily_one_challenge(challenge):
        date = challenge.started_at
        end_date = challenge.finished_at if challenge.is_finished else timezone.now().date()
        successful_periods = 0

        while date <= end_date:
            sum = challenge.progresses.filter(date__date=date).aggregate(sum=Sum('progress'))
            progress_sum = 0 if not sum.get('sum') else sum.get('sum')
            if progress_sum >= challenge.goal:
                successful_periods += 1
            date += timedelta(days=1)
        periods = (end_date - challenge.started_at).days + 1
        return periods, successful_periods

    @staticmethod
    def _get_count_periods_weekly(
            challenges, effective_challenge, effective_challenge_percent
    ):
        challenges = challenges.filter(period=Period.WEEK).all()
        print(Period.WEEK, len(challenges))
        return 0, 0, None, 0

    @staticmethod
    def _get_count_periods_monthly(
            challenges, effective_challenge, effective_challenge_percent
    ):
        challenges = challenges.filter(period=Period.MONTH).all()
        print(Period.MONTH, len(challenges))
        return 0, 0, None, 0
