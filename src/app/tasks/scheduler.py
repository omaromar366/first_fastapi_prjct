from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from app.core.db import SessionLocal
from app.services.calculate_delivery import calculate_delivery_for_all_parcels

scheduler = BackgroundScheduler()


def calculate_delivery_job() -> None:
    logger.info("Scheduler job started")
    db = SessionLocal()
    try:
        parcels = calculate_delivery_for_all_parcels(db=db)
        logger.info("Scheduler processed {} parcels", len(parcels))
    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler.get_job("calculate_delivery_job") is None:
        scheduler.add_job(
            calculate_delivery_job,
            trigger="interval",
            seconds=5,
            id="calculate_delivery_job",
        )

    if not scheduler.running:
        scheduler.start()
