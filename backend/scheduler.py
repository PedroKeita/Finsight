from apscheduler.schedulers.background import BackgroundScheduler
from collector import collect_all
from cache import invalidate_cache
import logging
import os

logger = logging.getLogger(__name__)

def scheduled_collect():
    """Job executado automaticamente para coletar dados de todos os ativos."""

    logger.info("Iniciando coleta automática agendada...")
    collect_all()
    invalidate_cache()
    logger.info("Coleta automática concluída!!!!")

def start_scheduler():
    hour = int(os.getenv("SCHEDULER_HOUR", 18))
    minute = int(os.getenv("SCHEDULER_MINUTE", 0))

    scheduler =  BackgroundScheduler()
    scheduler.add_job(
        scheduled_collect,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_collect"
    )
    
    scheduler.start()
    logger.info(f"Scheduler iniciado — coleta agendada para {hour:02d}:{minute:02d}")
    
    return scheduler