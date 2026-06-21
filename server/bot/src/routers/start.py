from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def start(
    message: Message,
    command: CommandObject,
) -> None:
    await message.answer(command.args or "Сегодня без аргументов")
