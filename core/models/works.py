from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DB_PREFIX, BaseDbModel

if TYPE_CHECKING:
    from .vehicle import Vehicle


class WorkPattern(BaseDbModel):
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]


class Work(BaseDbModel):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}vehicles.id", ondelete="CASCADE")
    )
    vehicle: Mapped["Vehicle"] = relationship(back_populates="works")
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]
    work_type: Mapped[int]
    note: Mapped[str]
