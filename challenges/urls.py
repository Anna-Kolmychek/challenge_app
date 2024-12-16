from django.urls import path, include
from rest_framework import routers

from challenges.apps import ChallengesConfig
from challenges.views import ChallengeViewSet

app_name = ChallengesConfig.name

router = routers.DefaultRouter()
router.register(r'', ChallengeViewSet)

urlpatterns = [
    # path('', ___.as_view()),
    path('', include(router.urls))
] + router.urls
