from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .jobs.empty_log_notification import empty_log_notification


def build_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=empty_log_notification,
        trigger=CronTrigger.from_crontab("* * * * *"),
    )

    return scheduler
