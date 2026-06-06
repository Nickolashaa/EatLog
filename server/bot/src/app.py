from aiogram import Bot, Dispatcher

from .config import BOT_TOKEN
from .di.session import SessionMiddleware
from .di.users import UserServiceMiddleware
from .routers import start

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.middleware(SessionMiddleware())
dp.message.middleware(UserServiceMiddleware())

dp.include_router(start.router)
