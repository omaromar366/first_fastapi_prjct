import asyncio
from decimal import Decimal

import aiohttp
from loguru import logger

from app.core.config import settings

MAX_RETRIES = 3
BACKOFF_FACTOR = 2


async def get_usd_rate() -> Decimal:
    """Fetch USD to RUB exchange rate from CBR API."""
    timeout = aiohttp.ClientTimeout(total=15)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(
                "Fetching USD rate from CBR API. Attempt {}/{}",
                attempt,
                MAX_RETRIES,
            )
            async with (
                aiohttp.ClientSession(timeout=timeout) as session,
                session.get(settings.cbr_url) as response,
            ):
                response.raise_for_status()
                data = await response.json(content_type=None)
                value = data["Valute"]["USD"]["Value"]

                logger.info("Fetched USD rate {} from CBR API", value)

                return Decimal(str(value))
        except (TimeoutError, aiohttp.ClientError) as exc:
            logger.warning(
                "Failed to fetch USD rate. Attempt {}/{}. Error: {}",
                attempt,
                MAX_RETRIES,
                exc,
            )
            if attempt == MAX_RETRIES:
                logger.exception("All attempts to fetch USD rate failed")
                raise Exception("Failed to fetch currency rate") from exc

            delay = BACKOFF_FACTOR ** (attempt - 1)

            logger.info("Retrying in {} seconds", delay)

            await asyncio.sleep(delay)

    raise RuntimeError("Failed to fetch currency rate")
