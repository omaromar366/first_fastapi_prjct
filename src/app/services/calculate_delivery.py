from sqlalchemy.orm import Session

from app.models import Parcel
from app.repositories.parcel import get_all_unpriced_parcels, get_unpriced_parcels_by_session_id
from app.services.currency import get_usd_to_rub_rate
from app.services.delivery_cost import calculate_delivery_cost


def calculate_delivery_for_parcels(db: Session, session_id: str) -> list[Parcel]:
    parcels = get_unpriced_parcels_by_session_id(db, session_id)
    usd_rate = get_usd_to_rub_rate()

    for parcel in parcels:
        delivery_cost = calculate_delivery_cost(
            weight=parcel.weight,
            declared_value_usd=parcel.declared_value_usd,
            usd_to_rub_rate=usd_rate,
        )
        parcel.delivery_cost_rub = delivery_cost

    db.commit()

    for parcel in parcels:
        db.refresh(parcel)

    return parcels


def calculate_delivery_for_all_parcels(db: Session) -> list[Parcel]:
    parcels = get_all_unpriced_parcels(db=db)
    usd_rate = get_usd_to_rub_rate()

    for parcel in parcels:
        delivery_cost = calculate_delivery_cost(
            weight=parcel.weight,
            declared_value_usd=parcel.declared_value_usd,
            usd_to_rub_rate=usd_rate,
        )
        parcel.delivery_cost_rub = delivery_cost

    db.commit()

    for parcel in parcels:
        db.refresh(parcel)

    return parcels
