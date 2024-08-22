import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel, DB_PREFIX

if TYPE_CHECKING:
    from .vehicle import Vehicle
    from .works import Work


class Event(BaseDbModel):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}vehicles.id", ondelete="CASCADE")
    )
    vehicle: Mapped["Vehicle"] = relationship(back_populates="events")
    work_date: Mapped[datetime.date]
    mileage: Mapped[int]
    work_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}works.id", ondelete="CASCADE")
    )
    work: Mapped["Work"] = relationship()
    part_price: Mapped[float]
    work_price: Mapped[float]
    note: Mapped[str]


class MileageEvent(BaseDbModel):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}vehicles.id", ondelete="CASCADE")
    )
    mileage_date: Mapped[datetime.date]
    mileage: Mapped[int]
