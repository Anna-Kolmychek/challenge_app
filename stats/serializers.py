import math
from collections import defaultdict
from datetime import timedelta

from django.db.models import Sum, ExpressionWrapper, F, DateField
from django.db.models.functions import TruncWeek
from rest_framework import serializers
from django.utils import timezone

from challenges.models import Period
from challenges.serializers import GetFinishedChallengeSerializer
from challenges import services
from challenges.services import get_challenge_end_date


class ChallengesSerializer(serializers.Serializer):
    """Serializer for `challenge` field description
    in CommonStatisticsSerializer, for display in drf-spectacular"""
    all = serializers.IntegerField()
    completed = serializers.IntegerField()


class PeriodStatsSerializer(serializers.Serializer):
    """Serializer for field description
    in PeriodsSerializer, for display in drf-spectacular"""
    day = serializers.IntegerField()
    week = serializers.IntegerField()
    month = serializers.IntegerField()


class PeriodsSerializer(serializers.Serializer):
    """Serializer for `periods` field description
    in CommonStatisticsSerializer, for display in drf-spectacular"""
    all_periods = PeriodStatsSerializer()
    successful_periods = PeriodStatsSerializer()


class EffectiveChallengeSerializer(serializers.Serializer):
    """Serializer for `effective_challenge` field description
    in CommonStatisticsSerializer, for display in drf-spectacular"""
    percent = serializers.FloatField()
    periods = serializers.IntegerField()
    successful_periods = serializers.IntegerField()
    challenge = GetFinishedChallengeSerializer()


class LongestChallengeSerializer(serializers.Serializer):
    """Serializer for `longest_challenge` field description
    in CommonStatisticsSerializer, for display in drf-spectacular"""
    duration = serializers.IntegerField()
    challenge = GetFinishedChallengeSerializer()


class CommonStatisticsSerializer(serializers.Serializer):
    """Serializer for common stats."""

    days_since_registration = serializers.IntegerField(min_value=1)
    challenges = ChallengesSerializer()
    periods = PeriodsSerializer()
    effective_challenge = EffectiveChallengeSerializer()
    longest_challenge = LongestChallengeSerializer()

    def to_representation(self, challenges):
        user = self.context.get('request').user

        days_since_registration = self._get_days_since_registration(user)
        count_all_challenges = self._get_count_all_challenges(challenges)
        count_completed_challenges = self._get_count_completed_challenges(
            challenges)

        longest_challenge = self._get_longest_challenge(challenges)

        periods_data, effective_challenge = self._get_count_periods(challenges)

        return {
            'days_since_registration': days_since_registration,

            'challenges': {
                'all': count_all_challenges,
                'completed': count_completed_challenges
            },

            'periods': periods_data,

            'effective_challenge': {
                'percent': effective_challenge['percent'],
                'periods': effective_challenge['periods'],
                'successful_periods': effective_challenge['successful_periods'],
                'challenge': GetFinishedChallengeSerializer(
                    effective_challenge['challenge']).data,
            },

            'longest_challenge': {
                'duration': longest_challenge['duration'],
                'challenge': GetFinishedChallengeSerializer(
                    longest_challenge['challenge']).data,

            },
        }

    @staticmethod
    def _get_days_since_registration(user):
        """Get the number of days since the user's registration."""

        return (timezone.now().date() - user.date_joined.date()).days + 1

    @staticmethod
    def _get_count_all_challenges(challenges):
        """Get the total number of challenges."""

        return len(challenges)

    @staticmethod
    def _get_count_completed_challenges(challenges):
        """Get the number of completed challenges."""

        return challenges.filter(is_finished=True).count()

    @staticmethod
    def _get_longest_challenge(challenges):
        """Get the longest challenge and its duration
        (counting the days for any periodicity)."""
        longest_challenge = {
            'challenge': None,
            'duration': 0,
        }

        for challenge in challenges:
            end_date = get_challenge_end_date(challenge)
            duration = (end_date - challenge.started_at).days + 1

            if duration > longest_challenge['duration']:
                longest_challenge['challenge'] = challenge
                longest_challenge['duration'] = duration

        return longest_challenge

    def _get_count_periods(self, challenges):
        """Get period statistics
        and the most effective challenge with its statistics."""

        period_names = (Period.DAY, Period.WEEK, Period.MONTH)
        all_periods = dict.fromkeys(period_names, 0)
        successful_periods = dict.fromkeys(period_names, 0)

        effective_challenge = {
            'challenge': None,
            'percent': 0.0,
            'periods': 0,
            'successful_periods': 0,
        }

        for challenge in challenges:
            ch_all_periods, ch_successful_periods = self._get_count_periods_one_challenge(
                challenge)
            all_periods[challenge.period] += ch_all_periods
            successful_periods[challenge.period] += ch_successful_periods

            if ch_all_periods > 0:
                percent = ch_successful_periods / ch_all_periods
                if percent > effective_challenge['percent']:
                    effective_challenge['challenge'] = challenge
                    effective_challenge['percent'] = percent
                    effective_challenge['periods'] = ch_all_periods
                    effective_challenge['successful_periods'] = ch_successful_periods

        periods = {
            'all_periods': all_periods,
            'successful_periods': successful_periods
        }

        return periods, effective_challenge

    def _get_count_periods_one_challenge(self, challenge):
        """Get statistics of periods for a single challenge
         (redirection by function depending on the periodicity)."""

        period_handlers = {
            Period.DAY: self._get_count_periods_daily,
            Period.WEEK: self._get_count_periods_weekly,
            Period.MONTH: self._get_count_periods_monthly,
        }

        handler = period_handlers.get(challenge.period)

        if not handler:
            raise serializers.ValidationError(
                f'Unsupported period {challenge.period} in challenge {challenge.uuid}'
            )

        return handler(challenge)

    @staticmethod
    def _get_count_periods_daily(challenge):
        """Get statistics of periods for a daily challenge."""

        start_date = challenge.started_at
        end_date = get_challenge_end_date(challenge)
        periods = (end_date - start_date).days + 1

        successful_periods = challenge.progresses.filter(
            date__date__gte=start_date,
            date__date__lte=end_date
        ).values('date__date').annotate(
            progress_sum=Sum('progress')
        ).filter(progress_sum__gte=challenge.goal).count()

        return periods, successful_periods

    @staticmethod
    def _get_count_periods_weekly(challenge):
        """Get statistics of periods for a weekly challenge."""

        start_date = challenge.started_at
        start_weekday = start_date.weekday()
        end_date = get_challenge_end_date(challenge)
        total_days = (end_date - start_date).days + 1
        periods = math.ceil(total_days / 7)

        successful_periods = challenge.progresses.filter(
            date__date__gte=start_date,
            date__date__lte=end_date
        ).annotate(
            shifted_date=ExpressionWrapper(
                F('date') - timedelta(days=start_weekday),
                output_field=DateField()
            ),
            week_start=TruncWeek('shifted_date')
        ).values('week_start').annotate(
            progress_sum=Sum('progress')
        ).filter(progress_sum__gte=challenge.goal).count()

        return periods, successful_periods

    @staticmethod
    def _get_count_periods_monthly(challenge):
        """Get statistics of periods for a monthly challenge."""

        start_date = challenge.started_at
        end_date = get_challenge_end_date(challenge)

        periods = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        if end_date.day > start_date.day:
            periods += 1

        successful_periods = 0

        for i in range(periods):
            period_month = (start_date.month - 1 + i) % 12 + 1
            period_year = start_date.year + (start_date.month - 1 + i) // 12
            period_start_date = services.get_period_start_date_month(
                challenge.started_at, period_year, period_month
            )
            period_end_date = services.get_period_end_date_month(
                challenge.started_at, period_year, period_month
            )
            progress = challenge.progresses.filter(
                date__date__gte=period_start_date,
                date__date__lte=period_end_date
            ).aggregate(
                progress_sum=Sum('progress')
            )

            progress = progress.get('progress_sum') if progress.get('progress_sum') else 0

            if progress >= challenge.goal:
                successful_periods += 1

        return periods, successful_periods
