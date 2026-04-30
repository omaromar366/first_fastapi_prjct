from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.session import get_or_create_session_id
from app.schemas.parcel import ParcelCreate, ParcelResponse
from app.services.calculate_delivery import calculate_delivery_for_parcels
from app.services.parcel import (
    create_parcel_for_session,
    get_parcel_by_id_for_session,
    get_parcels_for_session,
)

router = APIRouter()


@router.post("/parcels", response_model=ParcelResponse)
async def create_parcel_endpoint(
    parcel_data: ParcelCreate,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> ParcelResponse:
    session_id, is_new = get_or_create_session_id(request)
    logger.info(
        "Create parcel request received: session_id={}, name={}, type_id={}",
        session_id,
        parcel_data.name,
        parcel_data.type_id,
    )
    if is_new:
        logger.info("New session created: session_id={}", session_id)
        response.set_cookie(key="session_id", value=session_id)

    parcel = await create_parcel_for_session(db=db, parcel_data=parcel_data, session_id=session_id)
    logger.info(
        "Parcel created: id={}, session_id={}, name={}",
        parcel.id,
        session_id,
        parcel.name,
    )
    return parcel


@router.get("/parcels/{parcel_id}", response_model=ParcelResponse)
async def get_parcel_by_id_endpoint(
    parcel_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> ParcelResponse:
    session_id = request.cookies.get("session_id")
    logger.info(
        "Get parcel by id request: parcel_id={}, session_id={}",
        parcel_id,
        session_id,
    )

    if session_id is None:
        logger.warning("Get parcel by id failed: no session, parcel_id={}", parcel_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

    parcel = await get_parcel_by_id_for_session(db=db, parcel_id=parcel_id, session_id=session_id)

    if parcel is None:
        logger.warning(
            "Parcel not found: parcel_id={}, session_id={}",
            parcel_id,
            session_id,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcel not found",
        )
    logger.info(
        "Parcel returned: parcel_id={}, session_id={}",
        parcel.id,
        session_id,
    )

    return parcel


@router.get("/parcels", response_model=list[ParcelResponse])
async def get_parcels_endpoint(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    type_id: int | None = None,
    has_delivery_cost: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[ParcelResponse]:
    session_id = request.cookies.get("session_id")
    logger.info(
        "Get parcels request: session_id={}, limit={}, offset={}, type_id={}, has_delivery_cost={}",
        session_id,
        limit,
        offset,
        type_id,
        has_delivery_cost,
    )
    if session_id is None:
        logger.warning("Get parcels request without session")
        return []
    parcels = await get_parcels_for_session(
        type_id=type_id,
        limit=limit,
        offset=offset,
        db=db,
        session_id=session_id,
        has_delivery_cost=has_delivery_cost,
    )
    logger.info(
        "Returned {} parcels for session_id={}",
        len(parcels),
        session_id,
    )
    return parcels


@router.post("/parcels/calculate", response_model=list[ParcelResponse])
async def calculate_parcel_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> list[ParcelResponse]:
    session_id = request.cookies.get("session_id")
    logger.info("Calculate parcels request: session_id={}", session_id)

    if session_id is None:
        logger.warning("Calculate parcels failed: no session")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    parcels = await calculate_delivery_for_parcels(db=db, session_id=session_id)
    logger.info(
        "Calculated delivery cost for {} parcels, session_id={}",
        len(parcels),
        session_id,
    )

    return parcels
