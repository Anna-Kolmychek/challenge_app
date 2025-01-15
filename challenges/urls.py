from django.urls import path, include
from rest_framework import routers

from challenges.apps import ChallengesConfig
from challenges.views import ChallengeViewSet, ChallengeInProgressListAPIView

app_name = ChallengesConfig.name

router = routers.DefaultRouter()
router.register(r'', ChallengeViewSet)

urlpatterns = [
    path('in-progress/', ChallengeInProgressListAPIView.as_view()),
    path('', include(router.urls))
]
