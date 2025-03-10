from django.urls import path

from stats.apps import StatsConfig
from stats.views import CommonStatisticsAPIView

app_name = StatsConfig.name

urlpatterns = [
    path('common/', CommonStatisticsAPIView.as_view()),
]