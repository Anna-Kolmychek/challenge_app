import hashlib
import hmac
import json
from urllib.parse import parse_qs

from django.conf import settings
from rest_framework import exceptions, authentication

from users.models import CustomUser


class CustomAuthentication(authentication.BaseAuthentication):
    """Custom authentication by InitData from TG."""

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request)
        auth_header = auth_header.decode('utf-8')

        auth_header_components = auth_header.split()

        if len(auth_header_components) != 2:
            return None

        if auth_header_components[0] != 'tma':
            return None

        data = parse_qs(auth_header_components[1])
        init_data = {key: value[0] for key, value in data.items()}
        init_data_keys = sorted(init_data.keys())
        init_data_keys.remove('hash')
        init_data_str = '\n'.join(f'{key}={init_data[key]}' for key in init_data_keys)

        tg_bot_token_signature = hmac.new(
            b'WebAppData',
            settings.TG_BOT_TOKEN.encode('utf-8'),
            hashlib.sha256
        ).digest()

        init_data_signature = hmac.new(
            tg_bot_token_signature,
            init_data_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if init_data_signature != init_data.get('hash'):
            msg = 'Invalid InitData'
            raise exceptions.AuthenticationFailed(msg)

        if not init_data.get('user'):
            msg = 'Invalid InitData'
            raise exceptions.AuthenticationFailed(msg)

        user_data = json.loads(init_data.get('user'))

        if not user_data.get('id'):
            msg = 'Invalid InitData'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = CustomUser.objects.get(telegram_id=user_data.get('id'))
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                telegram_id=user_data.get('id'),
                username=user_data.get('username')
            )

        if not user.is_active:
            msg = 'User deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return user, None

    def authenticate_header(self, request):
        return 'telegram_id'
