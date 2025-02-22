from rest_framework import authentication, exceptions

from users.models import CustomUser


class CustomAuthentication(authentication.BaseAuthentication):
    """Custom authentication by telegram_id."""

    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request)
        auth_header = auth_header.decode('utf-8').lower()

        if not auth_header:
            return None

        if not auth_header.isdigit():
            return None

        try:
            user = CustomUser.objects.get(telegram_id=auth_header)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(telegram_id=auth_header)

        if not user.is_active:
            msg = 'User deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return user, None

    def authenticate_header(self, request):
        return 'telegram_id'
