from decimal import Decimal

import aiohttp
from loguru import logger

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def get_usd_rate() -> Decimal:
    logger.info("Fetching USD rate from CBR API")
    timeout = aiohttp.ClientTimeout(total=15)
    try:
        async with (
            aiohttp.ClientSession(timeout=timeout) as session,
            session.get(CBR_URL) as response,
        ):
            if response.status != 200:
                logger.error(
                    "Failed to fetch currency rate from CBR API. Status code: {}", response.status
                )
                raise Exception("Failed to fetch currency rate")

            data = await response.json(content_type=None)
    except TimeoutError as exc:
        logger.error("Timeout while fetching USD rate from CBR API")
        raise Exception("Currency API timeout") from exc
    usd_data = data["Valute"]["USD"]
    value = usd_data["Value"]
    logger.info("Fetched USD rate {} from CBR API", value)

    return Decimal(str(value))
