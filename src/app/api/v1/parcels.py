from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.session import get_or_create_session_id
from app.repositories.parcel import create_parcel, get_parcel_by_id, get_parcels
from app.schemas.parcel import ParcelCreate, ParcelResponse
from app.services.calculate_delivery import calculate_delivery_for_parcels

router = APIRouter()


@router.post("/parcels", response_model=ParcelResponse)
def create_parcel_endpoint(
    parcel_data: ParcelCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),  # noqa: B008
) -> ParcelResponse:
    session_id, is_new = get_or_create_session_id(request)
    if is_new:
        response.set_cookie(key="session_id", value=session_id)

    parcel = create_parcel(db=db, parcel_data=parcel_data, session_id=session_id)
    return parcel


@router.get("/parcels/{parcel_id}", response_model=ParcelResponse)
def get_parcel_by_id_endpoint(
    parcel_id: int,
    request: Request,
    db: Session = Depends(get_db),  # noqa: B008
) -> ParcelResponse:
    session_id = request.cookies.get("session_id")

    if session_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

    parcel = get_parcel_by_id(db=db, parcel_id=parcel_id, session_id=session_id)

    if parcel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcel not found",
        )

    return parcel


@router.get("/parcels", response_model=list[ParcelResponse])
def get_parcels_endpoint(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    type_id: int | None = None,
    has_delivery_cost: bool | None = None,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ParcelResponse]:
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return []
    parcels = get_parcels(
        type_id=type_id,
        limit=limit,
        offset=offset,
        db=db,
        session_id=session_id,
        has_delivery_cost=has_delivery_cost,
    )
    return parcels


@router.post("/parcels/calculate", response_model=list[ParcelResponse])
def calculate_parcel_endpoint(
    request: Request,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ParcelResponse]:
    session_id = request.cookies.get("session_id")

    if session_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    parcels = calculate_delivery_for_parcels(db=db, session_id=session_id)

    return parcels
