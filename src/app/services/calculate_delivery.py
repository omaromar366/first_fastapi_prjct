from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Parcel
from app.repositories.parcel import get_all_unpriced_parcels, get_unpriced_parcels_by_session_id
from app.services.currency import get_usd_to_rub_rate
from app.services.delivery_cost import calculate_delivery_cost


async def calculate_delivery_for_parcels(db: AsyncSession, session_id: str) -> list[Parcel]:
    parcels = await get_unpriced_parcels_by_session_id(db, session_id)
    usd_rate = await get_usd_to_rub_rate()

    for parcel in parcels:
        delivery_cost = calculate_delivery_cost(
            weight=parcel.weight,
            declared_value_usd=parcel.declared_value_usd,
            usd_to_rub_rate=usd_rate,
        )
        parcel.delivery_cost_rub = delivery_cost

    await db.commit()

    for parcel in parcels:
        await db.refresh(parcel)

    return parcels


async def calculate_delivery_for_all_parcels(db: AsyncSession) -> list[Parcel]:
    parcels = await get_all_unpriced_parcels(db=db)
    usd_rate = await get_usd_to_rub_rate()

    for parcel in parcels:
        delivery_cost = calculate_delivery_cost(
            weight=parcel.weight,
            declared_value_usd=parcel.declared_value_usd,
            usd_to_rub_rate=usd_rate,
        )
        parcel.delivery_cost_rub = delivery_cost

    await db.commit()

    for parcel in parcels:
        await db.refresh(parcel)

    return parcels
