import calendar
from datetime import timedelta, datetime

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers, exceptions

from challenges import services
from challenges.models import Challenge, Period
from progress.models import Progress


class BaseChallengeSerializer(serializers.ModelSerializer):
    """Base serializer for challenge."""

    class Meta:
        model = Challenge
        fields = (
            'id',
            'description',
            'goal',
            'period',
            'started_at',
            'finished_at',
        )


class CreateChallengeSerializer(BaseChallengeSerializer):
    """Serializer for creating challenge."""

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GetChallengeSerializer(BaseChallengeSerializer):
    """Serializer for get info on challenge."""

    progress = serializers.SerializerMethodField()

    class Meta(BaseChallengeSerializer.Meta):
        fields = BaseChallengeSerializer.Meta.fields + (
            'progress',
        )

    def get_progress(self, obj) -> int:
        started_date = services.get_started_date_for_current_progress(
            period=obj.period,
            started_at=obj.started_at
        )
        if not started_date:
            raise exceptions.ValidationError(
                {'started_at': f'The challenge{obj.id} has problems with the start date.'}
            )
        current_progress = Progress.objects.filter(
            challenge=obj, date__gte=started_date
        ).aggregate(sum=Sum('progress'))
        return current_progress.get('sum') if current_progress.get('sum') else 0


class UpdateChallengeSerializer(BaseChallengeSerializer):
    """Serializer for update info on challenge."""

    progress = serializers.IntegerField(write_only=True)

    class Meta(BaseChallengeSerializer.Meta):
        fields = BaseChallengeSerializer.Meta.fields + (
            'progress',
        )

    def update(self, instance, validated_data):
        new_progress = validated_data.pop('progress', None)
        if new_progress:
            total_progress = Progress.objects.filter(challenge=instance).aggregate(sum=Sum('progress'))
            old_progress = total_progress.get('sum') if total_progress.get('sum') else 0
            if new_progress > old_progress:
                Progress.objects.create(
                    challenge=instance,
                    progress=new_progress-old_progress,
                )
        instance = super().update(instance, validated_data)
        instance.refresh_from_db()
        print(new_progress)
        return self.to_representation(instance, new_progress)

    def to_representation(self, instance, new_progress=None):
        print(new_progress)
        representation = super().to_representation(instance)
        return {
            **representation,
            'progress': new_progress
        }



