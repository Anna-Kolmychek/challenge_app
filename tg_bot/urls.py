from django.urls import path

from tg_bot.apps import TgBotConfig
from tg_bot.views import TestTGAuth, InitDataListAPIView

app_name = TgBotConfig.name

urlpatterns = [
    path('test-auth/', TestTGAuth.as_view()),
    path('init-data/', InitDataListAPIView.as_view()),
]
