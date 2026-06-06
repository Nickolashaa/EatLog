from uuid import UUID

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

from ..services.exceptions import ObjectNotFound
from ..services.users.service import UserService

router = Router(name="start")


@router.message(CommandStart())
async def start(
    message: Message,
    command: CommandObject,
    user_service: UserService,
) -> None:
    if command.args is None:
        await message.answer(
            "Привет! Это бот EatLog для привязки аккаунта."
        )
        return

    arg = command.args.strip()
    if _is_int(arg):
        try:
            user = await user_service.get_by_telegram_id(int(arg))
        except ObjectNotFound:
            await message.answer("Пользователь не найден.")
            return
        await message.answer(f"Ваш UUID: {user.id}")
        return

    try:
        id = UUID(arg)
    except ValueError:
        await message.answer("Некорректный параметр.")
        return

    if message.from_user is None:
        return

    try:
        await user_service.register(id=id, telegram_id=message.from_user.id)
    except ObjectNotFound:
        await message.answer("Пользователь не найден.")
        return
    await message.answer("Вы успешно зарегистрированы!")


def _is_int(value: str) -> bool:
    return value.lstrip("-").isdigit()
