from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.parcel import create_parcel, get_parcel_by_id, get_parcels
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


@router.get("/parcels/{parcel_id}", response_model=ParcelResponse)
def get_parcel_by_id_endpoint(
    parcel_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> ParcelResponse:
    parcel = get_parcel_by_id(db=db, parcel_id=parcel_id)

    if parcel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcel not found",
        )

    return parcel


@router.get("/parcels", response_model=list[ParcelResponse])
def get_parcels_endpoint(
    limit: int = 10,
    offset: int = 0,
    type_id: int | None = None,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ParcelResponse]:
    parcels = get_parcels(type_id=type_id, limit=limit, offset=offset, db=db)
    return parcels
