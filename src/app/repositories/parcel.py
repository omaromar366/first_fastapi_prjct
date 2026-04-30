from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parcel import Parcel
from app.schemas.parcel import ParcelCreate


async def create_parcel(db: AsyncSession, parcel_data: ParcelCreate, session_id: str) -> Parcel:
    """Create parcel only if it belongs to session."""
    parcel = Parcel(
        name=parcel_data.name,
        weight=parcel_data.weight,
        type_id=parcel_data.type_id,
        declared_value_usd=parcel_data.declared_value_usd,
        session_id=session_id,
    )
    db.add(parcel)
    await db.commit()
    await db.refresh(parcel)
    return parcel


async def get_parcel_by_id(db: AsyncSession, parcel_id: int, session_id: str) -> Parcel | None:
    """Return parcel by id only if it belongs to session."""
    statement = select(Parcel).where(Parcel.id == parcel_id, Parcel.session_id == session_id)
    result = await db.execute(statement)
    parcel = result.scalar_one_or_none()
    return parcel


async def get_parcels(
    db: AsyncSession,
    session_id: str,
    limit: int,
    offset: int,
    type_id: int | None = None,
    has_delivery_cost: bool | None = None,
) -> list[Parcel]:
    """Return parcel only if it belongs to session."""
    statement = select(Parcel).where(Parcel.session_id == session_id)
    if type_id is not None:
        statement = statement.where(Parcel.type_id == type_id)
    if has_delivery_cost is True:
        statement = statement.where(Parcel.delivery_cost_rub.is_not(None))
    if has_delivery_cost is False:
        statement = statement.where(Parcel.delivery_cost_rub.is_(None))

    statement = statement.limit(limit).offset(offset)
    result = await db.execute(statement)
    parcels = list(result.scalars().all())
    return parcels


async def get_unpriced_parcels_by_session_id(db: AsyncSession, session_id: str) -> list[Parcel]:
    """Return parcels by session id only if it belongs to session."""
    statement = (
        select(Parcel)
        .where(Parcel.session_id == session_id)
        .where(Parcel.delivery_cost_rub.is_(None))
    )
    result = await db.execute(statement)
    parcels = list(result.scalars().all())
    return parcels


async def get_all_unpriced_parcels(db: AsyncSession) -> list[Parcel]:
    """Return unpriced parcels."""
    statement = select(Parcel).where(Parcel.delivery_cost_rub.is_(None))
    result = await db.execute(statement)
    parcels = list(result.scalars().all())
    return parcels
