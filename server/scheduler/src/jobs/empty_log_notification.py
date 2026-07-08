import random
from datetime import datetime
from logging import Logger, getLogger

from aiogram import Bot

from ..config import API_URL, BOT_TOKEN
from ..graphql.client import Client, GetUsersUsers, UsersFilterInput


async def _notify_users(
    logger: Logger,
    bot: Bot,
    users: list[GetUsersUsers],
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
                text=_build_text(name=users[i].name),
            )
            log += "SUCCESS"
            logger.info(log)
        except Exception as e:
            log += f"FAIL: {e}"
            logger.warning(log)


_TEXT_TEMPLATES = (
    "Привет, {name}! Сегодня ты ещё ничего не записал(а). Время добавить приём пищи 🍽️",
    "{name}, не забудь про EatLog! Записал(а) уже что-нибудь сегодня? 😉",
    "Эй, {name}! Твой дневник питания скучает. Добавь запись о еде за сегодня 📝",
    "Привет, {name}! Что было на обед? Не забудь занести это в дневник 🥗",
    "{name}, кажется, сегодня в логах пусто. Расскажи, что ты сегодня ел(а)? 🍎",
    "Доброго дня, {name}! Пара секунд — и приём пищи в дневнике. Не откладывай 🙌",
    "{name}, здоровые привычки любят регулярность. Запиши, что съел(а) сегодня! 💪",
    "Привет, {name}! Сегодня нет записей. Всё в порядке? Добавь еду в лог 🍲",
    "{name}, не теряй свой прогресс! Отметь сегодняшние приёмы пищи в EatLog ✨",
    "Хэй, {name}! Заполнишь дневник питания за сегодня? Это займёт минутку ⏱️",
    "Привет, {name}! Тело скажет спасибо за внимание к питанию. Добавь запись 🥑",
    "{name}, дневник ждёт! Что вкусного было сегодня в тарелке? 🍜",
    "Напоминаем, {name}: сегодня ещё нет ни одной записи о еде. Исправим? 🍳",
    "{name}, маленький шаг к цели — записать сегодняшнюю еду. Сделаем это вместе! 🎯",
    "Привет, {name}! Не дай дню пройти без записи в EatLog. Добавь приём пищи 🚀",
)


def _build_text(
    name: str,
) -> str:
    template = random.choice(_TEXT_TEMPLATES)
    return f"<b>Уведомление</b>\n\n{template.format(name=name)}"


async def empty_log_notification() -> None:
    logger = getLogger(__name__)
    client = Client(url=API_URL)
    bot = Bot(BOT_TOKEN)

    users = await client.get_users(
        filter_=UsersFilterInput(
            withoutLogsOn=datetime.now().date(),
            notificationTime=datetime.now().astimezone().timetz(),
            telegramIdExists=True,
        )
    )
    logger.info(f"Found {len(users)} users to be notified without logs")

    await _notify_users(
        logger=logger,
        bot=bot,
        users=users,
    )
