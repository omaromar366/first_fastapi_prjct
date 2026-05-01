from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.parcel_type import get_parcel_types
from app.schemas.parcel_type import ParcelTypeListResponse, ParcelTypeResponse

router = APIRouter()


@router.get("/parcel-types", response_model=ParcelTypeListResponse)
async def get_parcel_types_endpoint(
    db: AsyncSession = Depends(get_db),
) -> list[ParcelTypeResponse]:
    """Get parcel types endpoint."""
    parcel_types = await get_parcel_types(db)
    return ParcelTypeListResponse(items=parcel_types)
