from typing import Any, Tuple

from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
# from telegram_webapps_authentication import Authenticator

from users.models import CustomUser


class CustomAuthentication(BaseAuthentication):
    """Custom authentication. Get user by telegram_id from header
    Authorization: _telegram_id_"""

    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request)
        auth_header = auth_header.decode('utf-8').lower()

        if not auth_header:
            return None

        try:
            user = CustomUser.objects.get(telegram_id=auth_header)
        except CustomUser.DoesNotExist:
            msg = 'User not found'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return user, None

    def authenticate_header(self, request):
        return 'telegram_id'


# class TelegramInitDataAuthentication(BaseAuthentication):
#     """
#     Custom authentication class for validating Telegram WebApp InitData.
#
#     This class validates the `initData` received in the `Authorization`
#     header using the Telegram WebApps Authentication protocol. It extracts
#     the `telegram_id` from the validated data, which can be used for
#     user-related operations within the application.
#
#     Steps:
#     1. Retrieves `initData` from the `Authorization` header.
#     2. Uses the `Authenticator` class from the
#        `telegram-webapps-authentication` package to validate the `initData`.
#     3. If valid, extracts the `telegram_id` from the user data.
#     4. Returns the `telegram_id` if authentication is successful.
#
#     Raises:
#     - `AuthenticationFailed` if the `initData` is invalid, missing, or an
#       error occurs during validation.
#
#     Returns:
#     - A tuple containing the `telegram_id` and `None`.
#
#     Usage:
#     Include this class in the `authentication_classes` attribute of
#     specific Django REST Framework views to enable Telegram authentication.
#     """
#
#     def authenticate(self, request: Request) -> Tuple[str | None, Any | None]:
#         init_data: str | None = request.headers.get('Authorization')
#
#         if not init_data:
#             return None
#
#         authenticator = Authenticator(settings.BOT_TOKEN)
#         try:
#             if authenticator.validate_init_data(init_data):
#                 telegram_user = authenticator.get_telegram_user(init_data)
#                 telegram_id: str = telegram_user.id
#             else:
#                 raise AuthenticationFailed('Invalid InitData')
#         except Exception as e:
#             raise AuthenticationFailed(
#                 f'Error during InitData validation: {str(e)}'
#             )
#
#         return telegram_id, None
