import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DB_PREFIX, BaseDbModel
from .mixins import VehicleRelationMixin

if TYPE_CHECKING:
    from .works import Work


class Event(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "events"

    work_date: Mapped[datetime.date]
    mileage: Mapped[int]
    work_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}works.id", ondelete="CASCADE")
    )
    work: Mapped["Work"] = relationship()
    part_price: Mapped[float]
    work_price: Mapped[float]
    note: Mapped[str]


class MileageEvent(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "mileage_events"

    mileage_date: Mapped[datetime.date]
    mileage: Mapped[int]
