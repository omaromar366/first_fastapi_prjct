from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

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

    @field_serializer("delivery_cost_rub")
    def serialize_delivery_cost_rub(self, value: Decimal | None) -> str:
        if value is None:
            return "Не рассчитано"

        return str(value)

    model_config = ConfigDict(from_attributes=True)
