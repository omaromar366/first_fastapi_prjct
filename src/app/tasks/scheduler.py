from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.core.db import AsyncSessionLocal
from app.services.calculate_delivery import calculate_delivery_for_all_parcels

scheduler = AsyncIOScheduler()


async def calculate_delivery_job() -> None:
    """Calculate delivery cost for all unpriced parcels."""
    logger.info("Scheduler job started")
    try:
        async with AsyncSessionLocal() as db:
            parcels = await calculate_delivery_for_all_parcels(db=db)

        logger.info("Scheduler processed {} parcels", len(parcels))

    except Exception:
        logger.exception("Scheduler job failed")


def start_scheduler() -> None:
    """Scheduler startup."""
    if scheduler.get_job("calculate_delivery_job") is None:
        scheduler.add_job(
            calculate_delivery_job,
            trigger="interval",
            minutes=5,
            id="calculate_delivery_job",
        )

    if not scheduler.running:
        scheduler.start()
