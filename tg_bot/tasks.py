import json
from datetime import timedelta

import requests
from django.utils import timezone

from challenges import services
from challenges.models import Period, Challenge
from config import settings
from users.models import CustomUser


def send_tg_messages():
    """Organizes the sending of reminders in TG"""

    users = CustomUser.objects.filter(is_active=True, is_superuser=False).all()
    for user in users:
        message = form_message(user)
        if message:
            send_message_to_user(user.telegram_id, message)


def send_message_to_user(user_id, message):
    """Send message to user"""

    user_id = 1403132885
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'

    keyboard = {
        'inline_keyboard': [
            [
                {
                    'text': 'Открыть приложение',
                    'url': 'https://t.me/challengeUApp_bot/mychallenges'
                    # 'web_app': {
                    #     'url': 'https://t.me/challengeUApp_bot/mychallenges'
                    # }
                }
            ]
        ]
    }

    data = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps(keyboard),
    }

    response = requests.post(url, data=data)
    # ДОБАВИТЬ ЛОГИ на не отправленные сообщения


def form_message(user):
    challenges = Challenge.objects.filter(user=user, is_finished=False).all()
    # message = f'{user.telegram_id}\n'
    message = ''

    possible_periods = [Period.DAY, Period.WEEK, Period.MONTH]
    ch_dict = {}
    for period in possible_periods:
        ch_dict[period] = {
            'not_ready': '',
            'ready': '',
        }

    for challenge in challenges:
        period_finished_at = services.get_period_finished_at(
            challenge.started_at, challenge.finished_at, challenge.period
        )

        if (challenge.period == Period.WEEK and
                period_finished_at != (timezone.now() + timedelta(days=2)).date()):
            continue
        if (challenge.period == Period.MONTH and
                period_finished_at != (timezone.now() + timedelta(weeks=2)).date()):
            continue

        current_progress = services.get_current_progress(challenge)
        if current_progress < challenge.goal:
            num = ch_dict[challenge.period]['not_ready'].count('\n') + 1
            ch_dict[challenge.period]['not_ready'] += (
                f'{num}. {challenge.description} '
                f'({current_progress}/{challenge.goal})\n'
            )
            num += 1
        else:
            ch_dict[challenge.period]['ready'] += (
                f'\u2705 {challenge.description} '
                f'({current_progress}/{challenge.goal})\n'
            )

    if ch_dict[Period.DAY]['not_ready'] or ch_dict[Period.DAY]['ready']:
        message += 'Напоминаю о твоих <b><u>ежедневных</u></b> челленджах:\n'
        message += ch_dict[Period.DAY]['not_ready']
        message += ch_dict[Period.DAY]['ready']
        message += '\n'

    if ch_dict[Period.WEEK]['not_ready'] or ch_dict[Period.WEEK]['ready']:
        message += 'У этих <b><u>еженедельных</u></b> челленждей текущий период заканчивается через <b>2 дня</b>:\n'
        message += ch_dict[Period.WEEK]['not_ready']
        message += ch_dict[Period.WEEK]['ready']
        message += '\n'

    if ch_dict[Period.MONTH]['not_ready'] or ch_dict[Period.MONTH]['ready']:
        message += 'У этих <b><u>ежемесячных</u></b> челленждей текущий период заканчивается через <b>2 недели</b>:\n'
        message += ch_dict[Period.MONTH]['not_ready']
        message += ch_dict[Period.MONTH]['ready']

    return message
