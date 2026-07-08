from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .empty_log_notification import empty_log_notification

scheduler = AsyncIOScheduler()
scheduler.add_job(
    func=empty_log_notification,
    trigger=CronTrigger.from_crontab("* * * * *"),
)
