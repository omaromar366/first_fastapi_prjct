from decimal import ROUND_HALF_UP, Decimal


def calculate_delivery_cost(
    weight: Decimal, declared_value_usd: Decimal, usd_to_rub_rate: Decimal
) -> Decimal:
    base_cost = weight * Decimal("0.5") + declared_value_usd * Decimal("0.01")
    delivery_cost = base_cost * usd_to_rub_rate
    return delivery_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
