from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ParcelType


async def get_parcel_types(db: AsyncSession) -> list[ParcelType]:
    statement = select(ParcelType)
    result = await db.execute(statement)
    parcel_types = list(result.scalars().all())
    return parcel_types
