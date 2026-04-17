from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

if TYPE_CHECKING:
    from app.models.parcel_type import ParcelType


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("parcel_types.id"), nullable=False)
    declared_value_usd: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
    delivery_cost_rub: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now(), nullable=False
    )

    parcel_type: Mapped["ParcelType"] = relationship("ParcelType", back_populates="parcels")
