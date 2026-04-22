from decimal import Decimal

import httpx

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_usd_rate() -> Decimal:
    response = httpx.get(CBR_URL, timeout=5.0)

    if response.status_code != 200:
        raise Exception("Failed to fetch currency rate")

    data = response.json()

    usd_data = data["Valute"]["USD"]
    value = usd_data["Value"]

    return Decimal(str(value))
