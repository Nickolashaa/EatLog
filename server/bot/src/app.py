from aiogram import Bot, Dispatcher
from gql.client import Client

from .config import API_URL, BOT_TOKEN
from .routers import start

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp["gql_client"] = Client(url=API_URL)


dp.include_router(start.router)
