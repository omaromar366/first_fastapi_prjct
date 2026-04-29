from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.parcel_type import get_parcel_types
from app.schemas.parcel_type import ParcelTypeResponse

router = APIRouter()


@router.get("/parcel-types", response_model=list[ParcelTypeResponse])
async def get_parcel_types_endpoint(
    db: AsyncSession = Depends(get_db),
) -> list[ParcelTypeResponse]:
    parcel_types = await get_parcel_types(db)
    return parcel_types
