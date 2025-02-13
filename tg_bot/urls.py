from django.urls import path

from tg_bot.apps import TgBotConfig
from tg_bot.views import TestTGAuth

app_name = TgBotConfig.name

urlpatterns = [
    path('test-auth/', TestTGAuth.as_view()),
]
