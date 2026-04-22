from apscheduler.schedulers.background import BackgroundScheduler

from app.core.db import SessionLocal
from app.services.calculate_delivery import calculate_delivery_for_all_parcels

scheduler = BackgroundScheduler()


def calculate_delivery_job() -> None:
    db = SessionLocal()
    try:
        calculate_delivery_for_all_parcels(db=db)
    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler.get_job("calculate_delivery_job") is None:
        scheduler.add_job(
            calculate_delivery_job,
            trigger="interval",
            minutes=5,
            id="calculate_delivery_job",
        )

    if not scheduler.running:
        scheduler.start()
