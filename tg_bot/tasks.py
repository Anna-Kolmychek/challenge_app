from telegram import Bot, error

from config import settings


async def send_tg_messages():
    bot = Bot(token=settings.TG_BOT_TOKEN)
    try:
        await bot.send_message('1403132885', 'test msg')
    except Exception as e:
        print(e)
