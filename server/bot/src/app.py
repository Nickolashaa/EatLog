from aiogram import Bot, Dispatcher

from .config import BOT_TOKEN
from .routers import start

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(start.router)
