from aiogram import Bot

from ..config import BOT_TOKEN


def get_bot() -> Bot:
    return Bot(BOT_TOKEN)
