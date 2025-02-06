import calendar
from datetime import timedelta, datetime

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers, exceptions

from challenges import services
from challenges.models import Challenge, Period, PatchData
from progress.models import Progress


class BaseChallengeSerializer(serializers.ModelSerializer):
    """Base serializer for challenge."""
    is_finished = serializers.BooleanField(default=False)

    class Meta:
        model = Challenge
        fields = (
            'uuid',
            'description',
            'goal',
            'period',
            'started_at',
            'finished_at',
            'is_finished',
        )


class CreateChallengeSerializer(BaseChallengeSerializer):
    """Serializer for creating challenge."""

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GetChallengeSerializer(BaseChallengeSerializer):
    """Serializer for get info on active challenge."""

    progress = serializers.SerializerMethodField()
    period_finished_at = serializers.SerializerMethodField()

    class Meta(BaseChallengeSerializer.Meta):
        fields = BaseChallengeSerializer.Meta.fields + (
            'progress',
            'period_finished_at',
        )

    def get_progress(self, obj) -> int:
        return services.get_current_progress(obj)

    def get_period_finished_at(self, obj) -> int:
        period_finished_at = None
        if obj.period == Period.MONTH:
            period_finished_at = services.get_period_finished_at(obj.started_at)
        return period_finished_at


class UpdateChallengeSerializer(BaseChallengeSerializer):
    """Serializer for update info on challenge."""

    progress = serializers.IntegerField(min_value=0)

    class Meta(BaseChallengeSerializer.Meta):
        fields = BaseChallengeSerializer.Meta.fields + (
            'progress',
        )

    def update(self, instance, validated_data):

        # ------------------------------- start
        # print(str(validated_data))
        PatchData.objects.create(
            body=str(validated_data),
            challenges_uuid=instance.uuid,
            challenges_desc=instance.description,
        )

        # ------------------------------- finish

        new_progress = validated_data.pop('progress', None)
        is_finished = validated_data.get('is_finished', None)

        if is_finished == True and instance.is_finished == False:
            validated_data['finished_at'] = timezone.now().date()

        instance = super().update(instance, validated_data)

        if new_progress is not None:
            current_progress = services.get_current_progress(instance)
            if new_progress > current_progress:
                Progress.objects.create(
                    challenge=instance,
                    progress=new_progress - current_progress,
                )
            elif new_progress < current_progress:
                services.reduce_current_progress(
                    challenge=instance,
                    del_progress=current_progress - new_progress,
                )

            instance.progress = new_progress
        else:
            instance.progress = services.get_current_progress(instance)

        return instance


class GetFinishedChallengeSerializer(BaseChallengeSerializer):
    """Serializer for get info on finished challenge."""

    total_progress = serializers.SerializerMethodField(read_only=True)
    goal_progress = serializers.SerializerMethodField(read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseChallengeSerializer.Meta):
        fields = BaseChallengeSerializer.Meta.fields + (
            'total_progress',
            'goal_progress',
            'duration',
        )

    def get_total_progress(self, obj):
        total_progress = Progress.objects.filter(
            challenge=obj,
        ).aggregate(sum=Sum('progress'))
        return total_progress.get('sum') if total_progress.get('sum') else 0

    def get_goal_progress(self, obj):
        duration_days = self.get_duration(obj)
        goal_progress = None
        if obj.period == Period.DAY:
            goal_progress = duration_days * obj.goal
        elif obj.period == Period.WEEK:
            duration_weeks = duration_days / 7
            goal_progress = int(duration_weeks * obj.goal)
        elif obj.period == Period.MONTH:
            duration_months = duration_days / 30.44
            goal_progress = int(duration_months * obj.goal)

        return goal_progress

    def get_duration(self, obj):
        try:
            duration = (obj.finished_at - obj.started_at).days + 1
        except Exception:
            raise exceptions.ValidationError({'date': f'incorrect dates for the challenge {obj.id}'})
        return duration
