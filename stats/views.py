from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from challenges import services
from challenges.models import Challenge
from stats.serializers import CommonStatisticsSerializer


class CommonStatisticsAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        services.finish_completed_challenges(self.request.user)
        challenges = Challenge.objects.filter(
            user=self.request.user,
        ).all()
        serializer = CommonStatisticsSerializer(challenges, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
