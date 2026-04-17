from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.parcel_type import ParcelTypeResponse


class ParcelCreate(BaseModel):
    name: str
    weight: Decimal = Field(gt=0)
    type_id: int = Field(gt=0)
    declared_value_usd: Decimal = Field(gt=0)


class ParcelResponse(BaseModel):
    id: int
    name: str
    weight: Decimal
    declared_value_usd: Decimal
    delivery_cost_rub: Decimal | None
    parcel_type: ParcelTypeResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
