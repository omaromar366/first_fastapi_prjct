from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.parcel_type import get_parcel_types
from app.schemas.parcel_type import ParcelTypeResponse

router = APIRouter()


@router.get("/parcel-types", response_model=list[ParcelTypeResponse])
def get_parcel_types_endpoint(
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ParcelTypeResponse]:
    parcel_types = get_parcel_types(db)
    return parcel_types
