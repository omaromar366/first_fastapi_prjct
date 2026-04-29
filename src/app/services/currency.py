from decimal import Decimal

from loguru import logger

from app.clients.cbr import get_usd_rate
from app.core.redis import redis_client

USD_RATE_CACHE_KEY = "usd_to_rub_rate"

USD_RATE_TTL = 300


async def get_usd_to_rub_rate() -> Decimal:
    try:
        cached_rate = await redis_client.get(USD_RATE_CACHE_KEY)
    except Exception:
        cached_rate = None

    if cached_rate is not None:
        logger.info("Currency cache hit for key {}", USD_RATE_CACHE_KEY)
        return Decimal(cached_rate)

    logger.info("Currency cache miss for key {}", USD_RATE_CACHE_KEY)
    usd_rate = await get_usd_rate()

    await redis_client.set(USD_RATE_CACHE_KEY, str(usd_rate), ex=USD_RATE_TTL)
    logger.info("Saved USD rate {} to Redis with TTL {} seconds", usd_rate, USD_RATE_TTL)

    return usd_rate
