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
