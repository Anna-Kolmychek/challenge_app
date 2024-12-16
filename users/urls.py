from django.urls import path

from users.apps import UsersConfig
from users.views import UserMeRetrieveAPIView


app_name = UsersConfig.name

urlpatterns = [
    path('me/', UserMeRetrieveAPIView.as_view()),
]
