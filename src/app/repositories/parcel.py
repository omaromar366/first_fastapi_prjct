from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.parcel import Parcel
from app.schemas.parcel import ParcelCreate


def create_parcel(db: Session, parcel_data: ParcelCreate, session_id: str) -> Parcel:
    parcel = Parcel(
        name=parcel_data.name,
        weight=parcel_data.weight,
        type_id=parcel_data.type_id,
        declared_value_usd=parcel_data.declared_value_usd,
        session_id=session_id,
    )
    db.add(parcel)
    db.commit()
    db.refresh(parcel)
    return parcel


def get_parcel_by_id(db: Session, parcel_id: int) -> Parcel:
    statement = select(Parcel).where(Parcel.id == parcel_id)
    result = db.execute(statement)
    parcel = result.scalar_one_or_none()
    return parcel


def get_parcels(db: Session, limit: int, offset: int, type_id: int | None = None) -> list[Parcel]:
    statement = select(Parcel)
    if type_id:
        statement = select(Parcel).where(Parcel.type_id == type_id)
    statement = statement.limit(limit).offset(offset)
    result = db.execute(statement)
    parcels = list(result.scalars().all())
    return parcels
