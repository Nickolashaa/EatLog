import socket

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from .config import BOT_TOKEN
from .di.session import SessionMiddleware
from .di.users import UserServiceMiddleware
from .routers import start

session = AiohttpSession()
session._connector_init["family"] = socket.AF_INET
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

dp.message.middleware(SessionMiddleware())
dp.message.middleware(UserServiceMiddleware())

dp.include_router(start.router)
