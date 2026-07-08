from datetime import datetime, timezone
from logging import Logger, getLogger

from aiogram import Bot

from ..config import BOT_TOKEN
from ..database.connection import session_maker
from ..services.meal_logs.service import MealLogService
from ..services.users.schemas import UserSchema
from ..services.users.service import UserService


async def _get_users(
    logger: Logger,
    user_service: UserService,
    meal_log_service: MealLogService,
) -> list[UserSchema]:
    users_to_be_notified = await user_service.get_list(
        notification_time=datetime.now(timezone.utc)
        .replace(second=0, microsecond=0)
        .timetz(),
        telegram_id_exists=True,
    )
    len_users_to_be_notified = len(users_to_be_notified)
    logger.info(f"Found {len_users_to_be_notified} users to be notified")
    if len_users_to_be_notified == 0:
        return []

    users_to_be_notified_without_logs = [
        user
        for user in users_to_be_notified
        if user.id
        not in set(
            [
                meal_log.user_id
                for meal_log in await meal_log_service.get_list(
                    date_filter=datetime.now(timezone.utc).date(),
                )
            ]
        )
    ]
    logger.info(
        f"Found {len(users_to_be_notified_without_logs)} "
        "users to be notified without logs"
    )
    return users_to_be_notified_without_logs


async def _notify_users(
    logger: Logger,
    bot: Bot,
    users: list[UserSchema],
) -> None:
    len_users_without_logs = len(users)
    for i in range(len_users_without_logs):
        log = f"Notification {i + 1}/{len_users_without_logs}: "
        try:
            telegram_id = users[i].telegram_id
            if telegram_id is None:
                log += "FAIL: Empty telegram id"
                logger.warning(log)
                continue

            await bot.send_message(
                chat_id=telegram_id,
                text=(f"<b>Уведомление</b>\n\nПривет, {users[i].name}! ?????"),
            )
            log += "SUCCESS"
            logger.info(log)
        except Exception as e:
            log += f"FAIL: {e}"
            logger.warning(log)


async def empty_log_notification() -> None:
    logger = getLogger(__name__)
    session = session_maker()
    user_service = UserService(session)
    meal_log_service = MealLogService(session)
    bot = Bot(BOT_TOKEN)

    try:
        await _notify_users(
            logger=logger,
            bot=bot,
            users=await _get_users(
                logger=logger,
                user_service=user_service,
                meal_log_service=meal_log_service,
            ),
        )
    finally:
        await session.close()
        await bot.session.close()
