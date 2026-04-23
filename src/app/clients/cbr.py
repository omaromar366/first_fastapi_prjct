from decimal import Decimal

import httpx
from loguru import logger

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_usd_rate() -> Decimal:
    logger.info("Fetching USD rate from CBR API")
    response = httpx.get(CBR_URL, timeout=5.0)

    if response.status_code != 200:
        logger.error(
            "Failed to fetch currency rate from CBR API. Status code: {}", response.status_code
        )
        raise Exception("Failed to fetch currency rate")

    data = response.json()

    usd_data = data["Valute"]["USD"]
    value = usd_data["Value"]
    logger.info("Fetched USD rate {} from CBR API", value)

    return Decimal(str(value))
