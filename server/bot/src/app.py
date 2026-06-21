from aiogram import Bot, Dispatcher

from .config import API_URL, BOT_TOKEN
from .graphql_client import Client
from .routers import start

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp["gql_client"] = Client(url=API_URL)


dp.include_router(start.router)
