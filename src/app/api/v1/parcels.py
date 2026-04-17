from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.parcel import create_parcel
from app.schemas.parcel import ParcelCreate, ParcelResponse

router = APIRouter()


@router.post("/parcels", response_model=ParcelResponse)
def create_parcel_endpoint(
    parcel_data: ParcelCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> ParcelResponse:
    session_id = "test-session"
    parcel = create_parcel(db=db, parcel_data=parcel_data, session_id=session_id)
    return parcel
