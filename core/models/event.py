import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import DB_PREFIX, BaseDbModel
from .mixins import VehicleRelationMixin


class Event(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "events"

    work_date: Mapped[datetime.date]
    mileage: Mapped[int]
    work_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}works.id", ondelete="CASCADE")
    )
    part_price: Mapped[float]
    work_price: Mapped[float]
    note: Mapped[str]
