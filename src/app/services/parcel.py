from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parcel import Parcel
from app.repositories.parcel import (
    create_parcel,
    get_parcel_by_id,
    get_parcels,
)
from app.schemas.parcel import ParcelCreate


async def create_parcel_for_session(
    db: AsyncSession,
    parcel_data: ParcelCreate,
    session_id: str,
) -> Parcel:
    return await create_parcel(
        db=db,
        parcel_data=parcel_data,
        session_id=session_id,
    )


async def get_parcel_by_id_for_session(
    db: AsyncSession,
    parcel_id: int,
    session_id: str,
) -> Parcel | None:
    return await get_parcel_by_id(
        db=db,
        parcel_id=parcel_id,
        session_id=session_id,
    )


async def get_parcels_for_session(
    db: AsyncSession,
    session_id: str,
    limit: int,
    offset: int,
    type_id: int | None = None,
    has_delivery_cost: bool | None = None,
) -> list[Parcel]:
    return await get_parcels(
        db=db,
        session_id=session_id,
        limit=limit,
        offset=offset,
        type_id=type_id,
        has_delivery_cost=has_delivery_cost,
    )
