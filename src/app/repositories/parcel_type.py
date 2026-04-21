from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ParcelType


def get_parcel_types(db: Session) -> list[ParcelType]:
    statement = select(ParcelType)
    result = db.execute(statement)
    parcel_types = list(result.scalars().all())
    return parcel_types
