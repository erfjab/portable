from eiogram import Bot, Dispatcher
from ._env import TELEGRAM_API_TOKEN

BOT = Bot(token=TELEGRAM_API_TOKEN)
DP = Dispatcher(bot=BOT)
