from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, mixins, permissions, generics

from challenges.models import Challenge
from challenges import serializers as challenge_serializers, services


@extend_schema_view(
    create=extend_schema(summary='Create challenge'),
    retrieve=extend_schema(summary='Get challenge info by ID'),
    partial_update=extend_schema(summary='Update challenge info by ID'),
    destroy=extend_schema(summary='Delete challenge by ID'),
)
class ChallengeViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet,):
    """ViewsSet for Challenge: create, get by id, update by id, delete by id.\n
    Available only to authorized users.\n
    Only the current user's challenges are available.\n
    `"finished_at": null` means `all_time`"""

    http_method_names = ('get', 'post', 'patch', 'delete', )
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
    summary='Get all challenges in progress'
)
class ChallengeInProgressListAPIView(generics.ListAPIView):
    """Get a list of challenges in progress for the current user.\n
    Available only to authorized users."""

    queryset = Challenge.objects.all()
    serializer_class = challenge_serializers.GetChallengeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        services.finish_completed_challenges(self.request.user)

        challenges = Challenge.objects.filter(
            user=self.request.user,
            is_finished=False,
        ).all()

        challenges = services.custom_ordering(challenges)

        return challenges


@extend_schema(
    summary='Get all finished challenges'
)
class FinishedChallengeListAPIView(generics.ListAPIView):
    """Get a list of finished challenges for the current user.\n
    Available only to authorized users."""

    queryset = Challenge.objects.all()
    serializer_class = challenge_serializers.GetFinishedChallengeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        services.finish_completed_challenges(self.request.user)

        challenges = Challenge.objects.filter(
            user=self.request.user,
            is_finished=True,
        ).all()

        challenges = services.custom_ordering(challenges)

        return challenges
