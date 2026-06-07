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
    if message.from_user is None:
        return

    arg = command.args.strip() if command.args else ""

    if not arg:
        await message.answer("Привет! Это бот EatLog для привязки аккаунта.")
        return

    mode, _, payload = arg.partition("_")
    telegram_id = message.from_user.id

    if mode == "login":
        try:
            user = await user_service.get_by_telegram_id(telegram_id)
        except ObjectNotFound:
            await message.answer(
                "К этому Telegram не привязан аккаунт. "
                "Сначала зарегистрируйтесь в приложении и привяжите Telegram."
            )
            return
        await message.answer(
            f"Ваш UUID для входа:\n<code>{user.id}</code>\n\n"
            "Скопируйте его и вставьте в приложении.",
            parse_mode="HTML",
        )
        return

    if mode == "reg":
        try:
            id = UUID(payload)
        except ValueError:
            await message.answer("Некорректный параметр.")
            return
        try:
            await user_service.register(id=id, telegram_id=telegram_id)
        except ObjectNotFound:
            await message.answer("Пользователь не найден.")
            return
        await message.answer("Вы успешно зарегистрированы!")
        return

    await message.answer("Некорректный параметр.")
