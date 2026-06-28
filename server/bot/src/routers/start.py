import html
from uuid import UUID

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

from ..graphql.client import (
    Client,
    GetUserByTelegramIdUserByTelegramIdUser,
    UpdateUserInput,
    UpdateUserUpdateUserUser,
)

router = Router(name="start")


def parse_args(command: CommandObject) -> UUID | None:
    try:
        return UUID(command.args)
    except Exception:
        return None


@router.message(CommandStart())
async def start(
    message: Message,
    command: CommandObject,
    gql_client: Client,
) -> None:
    if message.from_user is None:
        return

    if command.args is None:
        get_data = await gql_client.get_user_by_telegram_id(
            telegram_id=str(message.from_user.id)
        )
        user = get_data.user_by_telegram_id

        if isinstance(user, GetUserByTelegramIdUserByTelegramIdUser):
            await message.answer(
                f"Привет, {html.escape(user.name)}!\n"
                f"Вот твой UUID: <code>{user.id}</code>",
                parse_mode=ParseMode.HTML,
            )
            return
        await message.answer("Привет, незнакомец! Как ты сюда попал?)")
        return

    id = parse_args(command)
    if id is None:
        return

    update_data = await gql_client.update_user(
        id=id,
        input=UpdateUserInput(telegramId=str(message.from_user.id)),
    )
    updated_user = update_data.update_user
    if isinstance(updated_user, UpdateUserUpdateUserUser):
        await message.answer(
            f"Регистрация успешна! Добро пожаловать, {updated_user.name}"
        )
        return
    await message.answer("Пользователь не найден, увы")
