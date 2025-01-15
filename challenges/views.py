from django.utils import timezone
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, mixins, permissions, generics

from challenges.models import Challenge
from challenges import serializers as challenge_serializers, services


@extend_schema_view(
    create=extend_schema(summary='Create challenge'),
    retrieve=extend_schema(summary='Get challenge info by ID - not finished'),
    partial_update=extend_schema(summary='Update challenge info by ID - not finished'),
)
class ChallengeViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet,):
    """ViewsSet for Challenge: create, get by id, update by id.\n
    Available only to authorized users.\n
    Only the current user's challenges are available.\n
    `"finished_at": null` means `all_time`"""

    http_method_names = ['get', 'post', 'patch']
    queryset = Challenge.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return challenge_serializers.CreateChallengeSerializer
        elif self.action == 'retrieve':
            return challenge_serializers.GetChallengeSerializer
        elif self.action == 'partial_update':
            return challenge_serializers.UpdateChallengeSerializer
        return challenge_serializers.BaseChallengeSerializer

    def get_queryset(self):
        return Challenge.objects.filter(user=self.request.user).all()


@extend_schema(
    summary='Get all challenges in progress - not finished'
)
class ChallengeInProgressListAPIView(generics.ListAPIView):
    """Get a list of challenges in progress for the current user.\n
    Available only to authorized users."""

    queryset = Challenge.objects.all()
    serializer_class = challenge_serializers.GetChallengeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        services.finish_completed_challenges(self.request.user)

        return Challenge.objects.filter(
            user=self.request.user,
            is_finished=False,
            started_at__lte=timezone.now()
        ).all()
