import html
from uuid import UUID

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from gql.client import (
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


def build_greeting(name: str, id: UUID) -> str:
    return (
        f"Привет, {html.escape(name)}!\n"
        f"Рад приветствовать тебя в сообществе EatLog!\n"
        f"Вот твой UUID: <code>{id}</code>"
    )


@router.message(CommandStart())
async def start(
    message: Message,
    command: CommandObject,
    gql_client: Client,
) -> None:
    if message.from_user is None:
        return

    if command.args is None:
        user = await gql_client.get_user_by_telegram_id(
            telegram_id=str(message.from_user.id)
        )

        if isinstance(user, GetUserByTelegramIdUserByTelegramIdUser):
            await message.answer(
                text=build_greeting(name=user.name, id=user.id),
                parse_mode=ParseMode.HTML,
            )
            return
        await message.answer("Привет, Незнакомец! Как ты сюда попал?)")
        return

    id = parse_args(command)
    if id is None:
        return

    updated_user = await gql_client.update_user(
        id=id,
        input=UpdateUserInput(telegramId=str(message.from_user.id)),
    )
    if isinstance(updated_user, UpdateUserUpdateUserUser):
        await message.answer(
            text=build_greeting(name=updated_user.name, id=updated_user.id),
            parse_mode=ParseMode.HTML,
        )
        return
    await message.answer("Пользователь не найден, увы")
