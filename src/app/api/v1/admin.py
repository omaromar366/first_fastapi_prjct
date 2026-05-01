from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.parcel import ParcelListResponse
from app.services.calculate_delivery import calculate_delivery_for_all_parcels

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/recalculate-deliveries", response_model=ParcelListResponse)
async def recalculate_deliveries_endpoint(
    db: AsyncSession = Depends(get_db),
) -> ParcelListResponse:
    parcels = await calculate_delivery_for_all_parcels(db=db)

    return ParcelListResponse(items=parcels)
