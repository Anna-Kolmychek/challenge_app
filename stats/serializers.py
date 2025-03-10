import math
from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models import Sum, ExpressionWrapper, F, IntegerField, DateField
from django.db.models.functions import TruncWeek
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
        count_completed_challenges = self._get_count_completed_challenges(
            challenges)

        longest_challenge = self._get_longest_challenge(challenges)

        periods_data, effective_challenge = self._get_count_periods(challenges)

        # return {
        #     'days_since_registration': days_since_registration,
        #
        #     'count_completed_challenges': count_completed_challenges,
        #     'count_all_challenges': count_all_challenges,
        #
        #     'count_all_periods_daily': periods_data['all_periods'][Period.DAY],
        #     'count_successfully_periods_daily': periods_data['successful_periods'][Period.DAY],
        #
        #     'count_all_periods_weekly': periods_data['all_periods'][Period.WEEK],
        #     'count_successfully_periods_weekly': periods_data['successful_periods'][Period.WEEK],
        #
        #     'count_all_periods_monthly': periods_data['all_periods'][Period.MONTH],
        #     'count_successfully_periods_monthly': periods_data['successful_periods'][Period.MONTH],
        #
        #     'effective_challenge_percent': effective_challenge['percent'],
        #     'effective_challenge': GetChallengeSerializer(
        #         effective_challenge['challenge']).data,
        #
        #     'longest_challenge_duration': longest_challenge['duration'],
        #     'longest_challenge': GetChallengeSerializer(
        #         longest_challenge['challenge']).data,
        #
        # }
        return {
            'days_since_registration': days_since_registration,

            'challenges': {
                'all': count_all_challenges,
                'completed': count_completed_challenges
            },

            'periods': periods_data,

            'effective_challenge': {
                'percent': effective_challenge['percent'],
                'challenge': GetChallengeSerializer(
                    effective_challenge['challenge']).data,
            },

            'longest_challenge': {
                'duration': longest_challenge['duration'],
                'challenge': GetChallengeSerializer(
                    longest_challenge['challenge']).data,

            },
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
        longest_challenge = {
            'challenge': None,
            'duration': 0,
        }

        for challenge in challenges:
            end_date = challenge.finished_at if challenge.is_finished else timezone.now().date()
            duration = (end_date - challenge.started_at).days + 1

            if duration > longest_challenge['duration']:
                longest_challenge['challenge'] = challenge
                longest_challenge['duration'] = duration

        return longest_challenge

    def _get_count_periods(self, challenges):
        all_periods = defaultdict(int)
        successful_periods = defaultdict(int)

        effective_challenge = {
            'challenge': None,
            'percent': 0.0
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

        periods = {
            'all_periods': all_periods,
            'successful_periods': successful_periods
        }

        return periods, effective_challenge

    def _get_count_periods_one_challenge(self, challenge):
        # Функции по периодам
        period_handlers = {
            Period.DAY: self._get_count_periods_daily,
            Period.WEEK: self._get_count_periods_weekly,
            Period.MONTH: self._get_count_periods_monthly,
        }

        # Получаем функцию из словаря
        handler = period_handlers.get(challenge.period)

        if not handler:
            raise serializers.ValidationError(
                f'Unsupported period {challenge.period} in challenge {challenge.uuid}'
            )

        return handler(challenge)

    @staticmethod
    def _get_count_periods_daily(challenge):
        start_date = challenge.started_at
        end_date = challenge.finished_at if challenge.is_finished else timezone.now().date()
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
        start_date = challenge.started_at
        start_weekday = start_date.weekday()
        end_date = challenge.finished_at if challenge.is_finished else timezone.now().date()
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
        return 0, 0
